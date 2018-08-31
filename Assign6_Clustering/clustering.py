#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Getting the list of words from the file
wordlist = list()
for line in open('wsj00-18.tag', 'r'):
    line = line.lower().strip().split()
    if line:
        wordlist.append(line[0])

# Collecting the 1000 most frequent words
freqwords = [word[0] for word in Counter(wordlist).most_common(1000)]

# Dictinaries to store counts of words to the left and right
left_count = {}
right_count = {}
for freqword in freqwords:
    left_count[freqword] = {}
    right_count[freqword] = {}

# Initialzing the left and right dictionaries for only one frequent word with all the words in the vocabulary and a count of 0.
# This step ensures that DictVectorizer produces vectors of length 38574 as mentioned in the sanity check. 
# However, I believe skipping these set of steps would not affect the clustering.
for freqword in freqwords:
    for word in set(wordlist):
        left_count[freqword][word] = 0
        right_count[freqword][word] = 0      
    break

# Get the left and right counts for the words surrounding the frequent words       
for i in range(0, len(wordlist)-1):
    if wordlist[i] in freqwords:
        left_count[wordlist[i]][wordlist[i-1]] = left_count[wordlist[i]].get(wordlist[i-1], 0) + 1
        right_count[wordlist[i]][wordlist[i+1]] = right_count[wordlist[i]].get(wordlist[i+1], 0) + 1

# Vectorizing the dictionaries using DictVectorizer
left_count_dict_list = [left_count[word] for word in freqwords]  # Collecting all the left count dicts into a list
right_count_dict_list = [right_count[word] for word in freqwords] # Collecting all the right count dicts into a list
v = DictVectorizer(sparse=False)
left_vectors = v.fit_transform(left_count_dict_list) 
right_vectors = v.fit_transform(right_count_dict_list)
vectors = [list(left_vectors[i])+list(right_vectors[i]) for i in range(0,len(freqwords))]  # concatenating the left and right vectors

# Normalizing the Vectors    
for i in range(0,len(vectors)):
    s = sum(vectors[i])
    vectors[i] = [float(x)/s for x in vectors[i]]

# Clustering
X = np.array(vectors)
n = 25
kmeans = KMeans(n_clusters=n, random_state=0).fit(X)
cluster_labels = kmeans.labels_

# Printing the individual Clusters
l = {}
for j in range(0, n):
    l[j] = []
    for i in range(0, len(freqwords)):
        if cluster_labels[i] == j:
            l[j].append(freqwords[i])
    print(str(j+1)+": " + " ".join(l[j]))