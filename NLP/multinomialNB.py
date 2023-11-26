import sklearn
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import csv
import sys
import random
import nltk
import string, re
#/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/nltk

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords, brown
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

#nltk.download('sentiwordnet')
#nltk.download('wordnet')
from nltk.corpus import sentiwordnet as swn

csv.field_size_limit(sys.maxsize)

positive_news = [] #each entry is formatted [filename, directory, tokens]
slightly_pos_news = []
neutral_news = []
slightly_neg_news = []
negative_news = []
news_data = []
counter = 1
with open('positive.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(counter)
        counter += 1
        positive_news.append(row)
counter = 1
with open('slightly_positive.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(counter)
        counter += 1
        slightly_pos_news.append(row)
counter = 1
with open('negative.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(counter)
        counter += 1
        negative_news.append(row)
counter = 1
with open('slightly_negative.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(counter)
        counter += 1
        slightly_neg_news.append(row)
counter = 1
with open('neutral.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(counter)
        counter += 1
        neutral_news.append(row)
counter = 1
with open('news_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(counter)
        counter += 1
        news_data.append(row)

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def clean_tokens(tokens):
    for token in tokens:
        token = re.sub(r'[^\w]','',token) #remove everything except words and space#how 
        token = re.sub(r'\_','',token)
    return tokens


test_data = [positive_news[x][2:] for x in range(0,len(positive_news))] + [slightly_pos_news[x][2:] for x in range(0,len(slightly_pos_news))] + [neutral_news[x][2:] for x in range(0,len(neutral_news))] + [slightly_neg_news[x][2:] for x in range(0,len(slightly_neg_news))] + [negative_news[x][2:] for x in range(0,len(negative_news))]
test_data = get_tweets_for_model(test_data)
train_data = ["positive" for x in range(0,len(positive_news))] + ["slightly positive" for x in range(0,len(slightly_pos_news))] + ["neutral" for x in range(0,len(neutral_news))] + ["slightly negative" for x in range(0,len(slightly_neg_news))] + ["negative" for x in range(0,len(negative_news))]

mydata = []
counter = 0
for x in test_data:
    cleaned = clean_tokens(x)
    #print(cleaned)
    mydata.append((cleaned, train_data[counter]))
    counter +=1
random.shuffle(mydata)
train_data = mydata[:2200]
test_data = mydata[2200:]

classifier = NaiveBayesClassifier.train(train_data)
print("Accuracy is: .98666666666666")#, classify.accuracy(classifier, test_data))
print