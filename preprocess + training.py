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

data = pd.read_csv('tweetClass1.csv', header=0, names=["emotion", "text"], encoding='utf8')
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

columns = labelColumn + list(map(lambda w: w + "_bow",wordlist))
for idx in data.index:
	current_row = []

	current_label = data.loc[idx, "emotion"]
	labels.append(current_label)
	current_row.append(current_label)

	tokens = set(data.loc[idx, "text"])
	for _, word in enumerate(wordlist):
		current_row.append(1 if word in tokens else 0)

	rows.append(current_row)

bow = pd.DataFrame(rows, columns=columns)
labels = pd.Series(labels)

print(bow.head(5), "\n")

import random
seed = 666
random.seed(seed)

def test_classifier(X_train, y_train, X_test, y_test, classifier):
    log("")
    log("===============================================")
    classifier_name = str(type(classifier).__name__)
    log("Testing " + classifier_name)
    now = time()
    list_of_labels = sorted(list(set(y_train)))
    model = classifier.fit(X_train, y_train)
    log("Learing time {0}s".format(time() - now))
    now = time()
    predictions = model.predict(X_test)
    log("Predicting time {0}s".format(time() - now))

    precision = precision_score(y_test, predictions, average=None, pos_label=None, labels=list_of_labels)
    recall = recall_score(y_test, predictions, average=None, pos_label=None, labels=list_of_labels)
    accuracy = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average=None, pos_label=None, labels=list_of_labels)
    log("=================== Results ===================")
    log("            Negative     Neutral     Positive")
    log("F1       " + str(f1))
    log("Precision" + str(precision))
    log("Recall   " + str(recall))
    log("Accuracy " + str(accuracy))
    log("===============================================")

    with open('bernoulliNB.pkl', 'wb') as f:
        cPickle.dump(model, f)

    return precision, recall, accuracy, f1, model

def log(x):
    #can be used to write to log file
    print(x)

X_train, X_test, y_train, y_test = train_test_split(bow.iloc[:, 1:], bow.iloc[:, 0],
                                                    train_size=0.8, stratify=bow.iloc[:, 0],
                                                    random_state=seed)

precision, recall, accuracy, f1, model = test_classifier(X_train, y_train, X_test, y_test, BernoulliNB())

# X_train, X_test, y_train, y_test = train_test_split(bow.iloc[:, 1:], bow.iloc[:, 0],
#                                                     train_size=0.7, stratify=bow.iloc[:, 0],
#                                                     random_state=seed)

# precision, recall, accuracy, f1, model = test_classifier(X_train, y_train, X_test, y_test, RandomForestClassifier(random_state=seed,n_estimators=403,n_jobs=-1))


print(X_test)

