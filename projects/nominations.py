from setup import nlp, stop_words
from utils import award_classifier, clean_tweet, string_similarity, get_awards_list, segregate_tweets_by_awardname
from constants import OFFICIAL_AWARDS_1315, OFFICIAL_AWARDS_1819
from collections import Counter
import re


def get_nominee_award(tweets, year):
    keyword = {"nom", "noms", 'nominee', 'nominees', 'nominate', 'nominated', 'nominating', 'nomination'}
    tweet_dict_by_award = segregate_tweets_by_awardname(keyword, tweets, year)
    
    awardcat = tweet_dict_by_award.keys()

    twitterwords = {"http", "rt", "goldenglobes", "golden", "globes", "globe", "goldenglobe"}
    stopWords = stop_words.union(twitterwords)
    new_stopWords = [award.split() for award in awardcat]
    award_stopwords = []
    for k in new_stopWords:
        award_stopwords = set(award_stopwords).union(set(k))
    new_stopWords = [i.lower() for i in award_stopwords]

    stopWords = stopWords.union(new_stopWords)

    present_dict_res_dict = {}
    for award, award_tweets in tweet_dict_by_award.items():
        present_dict_res_dict[award]=[]
        for tweet in award_tweets:
            cleaned_tweet = " ".join([word for word in tweet.split() if word.lower() not in stopWords])
            if not set(cleaned_tweet.split()).intersection(keyword):
                continue
            updated_tweet = " ".join([word for word in cleaned_tweet.split() if word.lower() not in keyword])
            doc = nlp(updated_tweet)
            for ent in doc.ents:
                present_dict_res_dict[award].append((ent.text,ent.label_))
    
    nominee_dict_res = {}
    for award, tweet_ents in present_dict_res_dict.items():
        a = Counter([ll[0].lower() for ll in tweet_ents if ll[1] in ["ORG", "WORK_OF_ART", "PERSON"]])
        cmp_l = [jackal[0] for jackal in list(a.most_common()[:20]) if jackal[1]] #not in ["NORP", "FAC", "GPE", "LOC", "PRODUCT", "EVENT", "LAW", "LANGUAGE", "DATE", "TIME", "PERCENT", "QUANTITY", "ORDINAL", "CARDINAL"]]
        nominee_dict_res[award] = cmp_l

    return nominee_dict_res