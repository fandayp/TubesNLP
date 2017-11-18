import json
import re
import nltk
import gensim
import pandas as pd
import numpy as np
import _pickle as cPickle
# from emoticons import EmoticonDetector
from collections import Counter
from time import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier

def remove_by_regex(tweets, regexp):
	tweets.loc[:, "text"].replace(regexp, "", inplace=True)
	return tweets

def remove_urls(tweets):
	return remove_by_regex(tweets, re.compile(r"http.?://[^\s]+[\s]?"))

def remove_na(tweets):
	return tweets[tweets["text"] != "Not Available"]

def remove_special_chars(tweets):
	for remove in map(lambda r: re.compile(re.escape(r)), [",", ":", "\"", "=", "&", ";", "%", "$", "@", "%", "^", "*", "(", ")", "{", "}", "[", "]", "|", "/", "\\", ">", "<", "-", "!", "?", ".", "'", "--", "---", "#", '~']):
		tweets.loc[:, "text"].replace(remove, "", inplace=True)
	
	return tweets

def remove_usernames(tweets):
	return remove_by_regex(tweets, re.compile(r"@[^\s]+[\s]?"))

def remove_numbers(tweets):
	return remove_by_regex(tweets, re.compile(r"\s?[0-9]+\.?[0-9]*"))

data = pd.read_csv('tweetTextFull.csv', header=0, names=["text"], encoding='utf8')
data = remove_urls(data)
data = remove_na(data)
data = remove_special_chars(data)
data = remove_usernames(data)
data = remove_numbers(data)

stemmer = nltk.PorterStemmer()

data['tokenized'] = data['text'].apply(word_tokenize) 
data['text'] = data['tokenized'].apply(lambda x : [stemmer.stem(y) for y in x])

stopwords=nltk.corpus.stopwords.words("english")
whitelist = ["n't", "not"]

words = Counter()
for idx in data.index:
    words.update(data.loc[idx, "text"])

for idx, stop_word in enumerate(stopwords):
    if stop_word not in whitelist:
        del words[stop_word]

# print(words.most_common(5))
wordlist = [k for k, v in words.most_common()]

labelColumn = ["label"]
labels = []
rows = []

columns = list(map(lambda w: w + "_bow",wordlist))
for idx in data.index:
	current_row = []

	# labels.append(current_label)
	# current_row.append(current_label)

	tokens = set(data.loc[idx, "text"])
	for _, word in enumerate(wordlist):
		current_row.append(1 if word in tokens else 0)

	rows.append(current_row)

bow = pd.DataFrame(rows, columns=columns)
# print(bow)
labels = pd.Series(labels)

with open('randomForest.pkl', 'rb') as f:
    model = cPickle.load(f)

prediction = model.predict(bow)

print(len(prediction))
with open('newTweet.csv') as json_data:
	d = json.load(json_data)

classifiedTweet = []
i = 0

print(len(d))

for item in d:
	classifiedTweet.append(
            {'tweetText':item['tweetText'],
            'location': item['location'],
            'tweetCreatedAt':item['tweetCreatedAt'],
            'username': item['username'],
            'authorName': item['authorName'],
			'nama_acara': item['nama_acara'],
			'sentiment': prediction[i]
            })
	# print(classifiedTweet, prediction[i], "\n")
	i += 1

data = json.dumps(classifiedTweet)
try:
	saveFile = open('classifiedTweet.csv', 'a')
	saveFile.write(data)
	saveFile.write('\n')
	saveFile.close()
except BaseException as e:
	print('failed ondata,', str(e))
	time.sleep(5)  
