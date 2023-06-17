import re
from utils import clean_tweet
from collections import Counter
from setup import nlp, stop_words


def get_awards_winners(tweets_data):
  pattern = '(best\s.*)(\sin\s|\-)+(.*)?(goes to|\sis\s|\sare\s)(.*)'
  result_arr = []
  x = re.compile(pattern, re.IGNORECASE)
  
  for record in tweets_data:
    y = x.findall(record)
    if y:
      result_arr.append(y)

  award_name_arr = ["".join([y for y in search_results[0][:3]]).lower().strip() for search_results in result_arr]
  award_winner_top = Counter(award_name_arr)
  award_winner_top_30 = [x[0] for x in award_winner_top.most_common()[:30]]

  winner_li = []
  index_dict = {}

  for x in range(len(result_arr)):
    if result_arr[x]:
      doc = nlp("".join([y for y in result_arr[x][0][4:]]).lower())
      for ent in doc.ents:
        winner_li.append((ent.text,ent.label_))
        if ent.text not in index_dict:
            index_dict[x] = [ent.text]
            # index_dict[x].append(ent.text)
  a = Counter([i[0] for i in winner_li if i[1]=="PERSON"])
  fin_awards = [x[0] for x in a.most_common()[:30]]
  result_award_winner = {}
  
  for winner in fin_awards:
      num_flag = False
      for num_ in winner[:len(winner)-1]:
            if num_.isdigit():
                  num_flag = True
                  break
      if num_flag:
            continue 
      for key, value in index_dict.items():
            if winner in value:
                  new_key = "".join([y for y in result_arr[key][0][:3]]).lower().strip()
                  if new_key not in result_award_winner:
                        result_award_winner[new_key] = set()
                  result_award_winner[new_key].add(winner)
  for item in award_winner_top_30:
        if item not in result_award_winner:
            result_award_winner[item] = set()
  return result_award_winner
                    



