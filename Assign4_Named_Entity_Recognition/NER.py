#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.feature_extraction import DictVectorizer
from sklearn import svm

train_file = 'eng.train'
test_file = 'eng.testa'
output_file = 'eng.guessa'

# Function to read a file and create a list of sentences
def readconll(file):
    lines = [line.strip() for line in open(file)]
    while lines[-1] == '':  # Remove trailing empty lines
        lines.pop()
    s = [x.split('_') for x in '_'.join(lines).split('__')]  # Quick split corpus into sentences
    return [[y.split() for y in x] for x in s]

# Function which returns a list of feature dictionaries for a sentence, where each dictionary contains the feature:value pairs for a word or Token.
def get_features(sentence):
    sentence_features = []
    for i in range(0,len(sentence)):
        word_features = {}                                         			# Feature dictionary for a word in the sentence
        # Features 
        word_features['Identity = ' + sentence[i][0]] = 1					# Identity of the word
        word_features['POS = ' + sentence[i][1]] = 1						# Part of Speech of the word
        if i != 0:
            word_features['Identity Prev = ' + sentence[i-1][0]] = 1		# Identity of the previous word in the sentence
            word_features['POS Prev = ' + sentence[i-1][1]] = 1 			# Part of Speech of the previous word in the sentence
        if i != len(sentence)-1:
            word_features['Identity Next = ' + sentence[i+1][0]] = 1		# Identity of the next word in the sentence
            word_features['POS Next = ' + sentence[i+1][1]] = 1 			# Part of Speech of the next word in the sentence
        for j in range(0,4):
            if j < len(sentence[i][0]):										
                word_features['Prefix = '+ sentence[i][0][:j+1]] = 1		# Prefixes of length <= 4
                word_features['Suffix = '+ sentence[i][0][-j-1:]] = 1		# Suffixes of length <= 4
        if sentence[i][0].isupper():
            word_features['is_upper'] = 1									# Is the word Upper case?
        if '-' in sentence[i][0]:
            word_features['has_hyphen'] = 1									# Presence of hyphen 
        sentence_features.append(word_features)
    return sentence_features

sentences_train = readconll(train_file)
y = []																		# Our class labels for the words
features = []																# List of all feature dictionaries
for sentence in sentences_train:
    features.extend(get_features(sentence))
    for i in range(0,len(sentence)):
        y.append(sentence[i][3])
        
vectorizer = DictVectorizer(sparse = True)
X = vectorizer.fit_transform(features)

clf = svm.LinearSVC()														# Use Linear SVM
clf.fit(X, y)																# Train Classifier

# Classify Test Set
sentences_test = readconll(test_file)
file = open(output_file, 'w') 
for sentence in sentences_test:
    sentence_features = get_features(sentence)
    for i in range(0,len(sentence)):
        sentence[i].extend(clf.predict(vectorizer.transform([ sentence_features[i] ])))
        file.write(' '.join(sentence[i]) +'\n')
    file.write('\n')
file.close()
