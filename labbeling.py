# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 15:01:18 2017

@author: Elvina
"""

from textblob import TextBlob 
newFile = []
i=1

buffer_to_write = "Lable,Tweet\n"
for line in open('tweetTextFull.csv','r', encoding='utf8').readlines():
    blob = TextBlob(line)
    if (blob.correct().sentiment.polarity >0):
        sentiment = 'positive'
    elif (blob.correct().sentiment.polarity <0):
        sentiment = 'negative'
    else:
    	sentiment = 'neutral'
    print(line, sentiment, i)
    i += 1
    buffer_to_write +=""+sentiment+","+line+""

print(buffer_to_write, file=open("tweetClass.csv","w", encoding="utf-8"))
