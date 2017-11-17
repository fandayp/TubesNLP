import pandas as pd
import re
import json
from pprint import pprint
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import os
import time


with open('inputTweet.txt') as data_file:
    data = json.load(data_file)

df = pd.read_csv('normalisationDictionary.txt', delimiter='\t')
dic = {}
for x in df.values:
    dic[x[0]] = x[1]

with open("../dictionary/id.stopwords.txt", "r") as ins:
    stopwords_id = []
    for line in ins:
        line = line.replace("\n", "")
        stopwords_id.append(line)

stop_words = set(stopwords.words('english'))
stop_words.update(stopwords_id)
pattern = re.compile(r'\b(' + '|'.join(dic.keys()) + r')\b')
result = []

for item in data:
    tweetPreProc = pattern.sub(lambda x: dic[x.group()], item["tweetText"])
    tweetPreProc = re.sub(r'[^\w\s]','',tweetPreProc)
    tweetPreProc = [i.lower() for i in wordpunct_tokenize(tweetPreProc) if i.lower() not in stop_words]
    tweetPreProc = ' '.join(tweetPreProc)
    item["tweetPreProc"] = tweetPreProc
    result.append(item)



fileName = "outputPreposes.txt"
print("True")
data = json.dumps(result)
try:
    saveFile = open(fileName, 'w')
    saveFile.write(data)
    saveFile.write('\n')
    saveFile.close()
except BaseException as e:
    print('failed ondata,', str(e))
    time.sleep(5)

