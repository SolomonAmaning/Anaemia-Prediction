from utils import clean_tweet
from nltk import word_tokenize, bigrams, trigrams
import re, nltk
from collections import Counter
from setup import nlp, stop_words

def get_host_names(tweet_data):
    if not tweet_data:
        return ""

    hostname_regex = re.compile(r'host.*')
    all_bigrams = []
    for tweet in tweet_data:
        re_result = hostname_regex.findall(tweet, re.IGNORECASE)
        if not re_result:
            continue
        word_tokens = word_tokenize(tweet)
        filtered_sentence = " ".join(word.lower() for word in [word_token for word_token in word_tokens if not word_token.lower(
        ) in stop_words])  # if len(i) > 1) #and string_similarity("golden globe",i.lower()) < 0.7 )
        filtered_sentence = clean_tweet(filtered_sentence)

        bigrams_ = list(bigrams(word_tokenize(filtered_sentence)))
        trigrams_ = list(trigrams(word_tokenize(filtered_sentence)))
        all_bigrams.extend(bigrams_)
        all_bigrams.extend(trigrams_)
        all_bigrams.append(filtered_sentence)

    
    grams_most_common = Counter(all_bigrams).most_common(10)
    entity_relations = [[(z.text, z.label_) for z in list(
        nlp(" ".join(common_entry[0])).ents)] for common_entry in grams_most_common]
    return [val.title() for val in [x[0] for x in [relation[0] for relation in entity_relations if relation][:5] if x[1] == "PERSON"][:2]]
