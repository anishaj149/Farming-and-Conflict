import sys 
print(sys.path) 
import nltk
#/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/nltk

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords, brown
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

#nltk.download('sentiwordnet')
#nltk.download('wordnet')
from nltk.corpus import sentiwordnet as swn

import re, string, random


#take out random unecessary characters, lemmatize word (reduce to a standard root form)
def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

#generates a list of all the words 
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

#generates a dictionary 
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

#trying brown corpus news
'''stop_words = stopwords.words('english')
print("started news classification")
news_fileids = brown.fileids(categories='news')
news_files = [brown.words(fileids = [fileid]) for fileid in news_fileids]
n_tokens = remove_noise(news_files[0], stop_words)'''


def get_scores(news_tokens):
    posi = 0
    neg = 0 
    obj = 0
    len_tokens = len(news_tokens)
    for token, tag in pos_tag(news_tokens):
        if tag == "NN": #getting part of speech 
            pos = 'n'
        elif tag == 'VB':
            pos = 'v'
        else:
            pos = 'a'
        #print(token, pos)

        words = swn.senti_synsets(token, pos) 
        '''if len(list(words)) == 0: 
            print("len of words as list: " + str(len(list(words))))
            print(list(words))
            len_tokens -= 1
            print("word not counted \n")
            continue'''
        
        for word1 in words:
            #word1 = list(words)[0] #index 0 is required to return the first result from the list of words in the synset. 
            posi += 2 * word1.pos_score() # multiplied so that words with feelings will have a greater impact
            neg += 2 * word1.neg_score()
            obj+=word1.obj_score() 

            break

    print(len_tokens)
    posi = posi/len_tokens
    neg = neg/len_tokens
    obj = obj/len_tokens
    print("Pos Score: " + str(posi) + "   Neg Score: " + str(neg) + "   obj Score: " + str(obj))


stop_words = stopwords.words('english')
print("started news classification")
news_fileids = brown.fileids(categories='news')
news_files = [brown.words(fileids = [fileid]) for fileid in news_fileids]
n1_tokens = remove_noise(open(r"news/Afric01-05/'Democratic' frenzy in the Arab world - a wind of change or just a mild breeze_.RTF", 'r').read(), stop_words) #remove_noise(news_files[0], stop_words)
n2_tokens = remove_noise(news_files[1], stop_words)
n3_tokens = remove_noise(news_files[2], stop_words)
print("article 1: " + ' '.join(news_files[0][:100]))
get_scores(n1_tokens)
print("article 2: " + ' '.join(news_files[1][:100]))
get_scores(n2_tokens)
print("article 3: " + ' '.join(news_files[2][:100]))
get_scores(n3_tokens)

'''if __name__ == "__main__":

    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    #tokenizing
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
    print("completed tokenization")

    #lemmatizing and cleaning words
    positive_cleaned_tokens_list = [remove_noise(tokens, stop_words) for tokens in positive_tweet_tokens]
    negative_cleaned_tokens_list = [remove_noise(tokens, stop_words) for tokens in negative_tweet_tokens]
    print("completed cleaning")

    #finding most common words
    all_pos_words = get_all_words(positive_cleaned_tokens_list)
    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))
    print("Frequency distribution for positive words completed")

    #creating dataset
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)
    positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
    negative_dataset = [(tweet_dict, "Negative")for tweet_dict in negative_tokens_for_model]
    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)
    train_data = dataset[:7000]
    test_data = dataset[7000:]
    print("dataset created")

    classifier = NaiveBayesClassifier.train(train_data)
    print("Accuracy is:", classify.accuracy(classifier, test_data))
    print(classifier.show_most_informative_features(10))

    custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."
    custom_tokens = remove_noise(word_tokenize(custom_tweet))
    print(custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))

    #trying brown corpus news
    print("started news classification")
    news_fileids = brown.fileids(categories='news')
    news_files = [brown.words(fileids = [fileid]) for fileid in news_fileids]
    news_tokens = remove_noise(news_files[0], stop_words)

    print(' '.join(news_files[0][:100]), classifier.classify(dict([token, True] for token in news_tokens)))

    news_tokens = remove_noise(news_files[1], stop_words)
    print(' '.join(news_files[1][:100]), classifier.classify(dict([token, True] for token in news_tokens)))

    news_tokens = remove_noise(news_files[2], stop_words)
    print(' '.join(news_files[2][:100]), classifier.classify(dict([token, True] for token in news_tokens)))'''


