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
import os, csv


#take out random unecessary characters, lemmatize word (reduce to a standard root form)
def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []
    tweet_tokens = tweet_tokens.split()
    for token, tag in pos_tag(tweet_tokens):
        #print(token)
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
        
        for word1 in words:
            #print(token)
            #print(word1)
            #word1 = list(words)[0] #index 0 is required to return the first result from the list of words in the synset. 
            posi += word1.pos_score() # multiplied so that words with feelings will have a greater impact
            neg += word1.neg_score()
            obj+=word1.obj_score() 
            break

    
    posi = posi/len_tokens *10
    neg = neg/len_tokens *10
    obj = obj/len_tokens
    #print("Pos Score: " + str(posi) + "   Neg Score: " + str(neg) + "   obj Score: " + str(obj))
    return (posi, neg, obj)


positive_news = []
slightly_pos_news = []
neutral_news = []
slightly_neg_news = []
negative_news = []
news_data = []

def classify_lexicon_data(article_name, scores, tokens, directory):
    if -.05 >scores[0] - scores[1] > -.15:
        slightly_neg_news.append([article_name, directory] +  tokens)
        return "slightly_negative"
    elif -.1 > scores[0] - scores[1]:
        negative_news.append([article_name, directory] + tokens)
        return "negative"
    elif 0.05 < scores[0] - scores[1] < .15:
        slightly_pos_news.append([article_name, directory] + tokens)
        return "slighly_positive"
    elif .1 < scores[0] - scores[1]:
        positive_news.append([article_name, directory] + tokens)
        return "positive"
    else: 
        neutral_news.append([article_name, directory] + tokens)
        return "neutral"


stop_words = stopwords.words('english')
rootDir = "/Users/anisha/Documents/iFARM/NLP/news"
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    if dirName == "/Users/anisha/Documents/iFARM/NLP/news": continue
    file_counter = 0
    for fname in fileList:
        if fname[-4:] != ".txt": continue
        #print('\t%s' % fname)
        #myfile = dirName + "/" + fname
        #print("textutil -convert txt \"%s\"" % myfile)
        #os.system("textutil -convert txt \"%s\"" % myfile)
        
        if file_counter <= 1000: 
            print(str(file_counter) + '\t%s' % fname)
            tokens = remove_noise(open((dirName + "/"+ fname), 'r').read(), stop_words)
            scores = get_scores(tokens)
            classification = classify_lexicon_data(fname, scores, tokens, dirName)
            file_counter += 1
        else: 
            print(str(file_counter) + '\t%s' % fname)
            tokens = remove_noise(open((dirName + "/"+ fname), 'r').read(), stop_words)
            news_data.append([fname, dirName] + tokens)
            file_counter += 1
        
print(len(positive_news), len(slightly_pos_news), len(neutral_news), len(slightly_neg_news), len(negative_news))

pi = [len(positive_news)/2400, len(slightly_pos_news)/2400, len(neutral_news)/2400, len(slightly_neg_news)/2400, len(negative_news)/2400]


'''with open("positive.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(positive_news)
with open("slightly_positive.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(slightly_pos_news)
with open("neutral.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(neutral_news)
with open("slightly_negative.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(slightly_neg_news)
with open("negative.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(negative_news)'''

alldata = []
for article in positive_news:
    alldata.append(["positive", article[1][-10:]])
for article in slightly_pos_news:
    alldata.append(["slightly_pos", article[1][-10:]])
for article in neutral_news:
    alldata.append(["neutral", article[1][-10:]])
for article in slightly_neg_news:
    alldata.append(["slightly_neg", article[1][-10:]])
for article in negative_news:
    alldata.append(["negative", article[1][-10:]])

with open("alldata.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(alldata)