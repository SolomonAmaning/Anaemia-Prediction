from setup import nlp, stop_words
from utils import segregate_tweets_by_awardname
from constants import OFFICIAL_AWARDS_1315, OFFICIAL_AWARDS_1819
from collections import Counter

def getPresenters(tweet_data, year):
    keyword = {'present', 'presenting', 'presented', 'presents', 'presenter', 'presenters',
               'introduce', 'introducing', 'introduces', 'introduced',
               'announce', 'announcing', 'announces', 'announces', "introduction"}
    tweet_awardname_map = segregate_tweets_by_awardname(keyword, tweet_data, year)

    present_dict_res = []
    present_dict_res_dict = {}
    
    for awardname, tweets in tweet_awardname_map.items():
        present_dict_res_dict[awardname]=[]
        for text in tweets:
            doc = nlp(text)
            for ent in doc.ents:
                present_dict_res.append((ent.text,ent.label_))
                present_dict_res_dict[awardname].append((ent.text,ent.label_))

    result_dict_presenter = {}
    for awardname, tweets_entity in present_dict_res_dict.items():
        person_entities_counts = Counter([entry[0].lower() for entry in tweets_entity if entry[1]=="PERSON"])
        person_entities = [jackal[0] for jackal in list(person_entities_counts.most_common())][:12]
        result_dict_presenter[awardname] = person_entities

    return result_dict_presenter
