import math
import numpy as np
text = open('wsj00-18.tag', 'r')
sentence_list = []				# A list of sentences where each sentence is a set of tag-word pair for every word(or tag) in the sentence
tag_set = set(['<s>','</s>'])   # set of all tags
word_set = set()				# A set to store all the words in the training data
		
# code to loop through every sentence in the text, pad them with <s> and </s> and add the sentence to the sentence list
sentence = [{'<s>': ''}]
for line in text:
    word_tag = line.strip().split()
    # keep adding tag:word pair to the sentence till an empty line is encountered
    if word_tag:   
        sentence.append({word_tag[1]: word_tag[0]})
        tag_set.add(word_tag[1])
        word_set.add(word_tag[0])
    # when an empty line is encountered, pad the sentence with </s> and add the sentence to the sentence list
    else: 		   
        sentence.append({'</s>':''})
        sentence_list.append(sentence)
        sentence = [{'<s>': ''}]

# code to calculate the transition, emission and tag counts
transition_count = {}
emission_count = {}
tag_count = {}
for tag in tag_set:
    transition_count[tag] = {}
    emission_count[tag] = {}
    tag_count[tag] = 0
for sentence in sentence_list:
    for i in range(0,len(sentence)-1):
        tag1 = ''.join(sentence[i].keys())
        tag2 = ''.join(sentence[i+1].keys())
        word = ''.join(sentence[i].values())
        if i == 0:
            tag_count[tag1] += 1
        tag_count[tag2] += 1
        if tag2 in transition_count[tag1]:
            transition_count[tag1][tag2] += 1    # Count(tag2|tag1)
        else:
            transition_count[tag1][tag2] = 1      
        if word in emission_count[tag1]:
            emission_count[tag1][word] += 1 	 # Count(word|tag1)
        else:
            emission_count[tag1][word] = 1

# code to calculate the transition and emission probabilities
transition_prob = {}
emission_prob = {}
for tag1 in tag_set:
    transition_prob[tag1] = {}
    emission_prob[tag1] ={}
    for tag2 in tag_set:
        transition_prob[tag1][tag2] = (transition_count[tag1].get(tag2,0))/(tag_count[tag1])  # P(tag2|tag1)
    for word in word_set:
        emission_prob[tag1][word] = (emission_count[tag1].get(word,0))/(tag_count[tag1])	  # P(word|tag1)

# Viterbi function to output the most probable path
def viterbi(sentence, transition_prob, emission_prob, tag_set):
    state = ['<s>']
    for x in tag_set - set(['<s>', '</s>']):
        state.append(x)
    state.append('</s>')								# A list which stores the all the tags where the first tag is <s> and the last tag is </s>
    v = np.zeros((len(state), len(sentence)+2))			# A matrix to which stores the v[i][j] where i is the state and j is the time t (here t is the current word)
    
    # A matrix to store the back pointers (In this case, stores the state of the previous node)
    path = np.zeros((len(state), len(sentence)+2),dtype='int')

    # Intialization
    v[0][0] = 1
    for i in range(1, len(state)):     
        v[i][0] = 0

    # Iteration
    for j in range(1, len(sentence)+1):
        for i in range(1, len(state)):
            v[i][j] = 0
            k_lower_bound = 0
            if j != 1:
                k_lower_bound = 1
            for k in range(k_lower_bound,len(state)):
                v_temp = v[k][j-1]*transition_prob[state[k]][state[i]]*emission_prob[state[i]][sentence[j-1]]
                if v[i][j] < v_temp:
                    v[i][j] = v_temp
                    path[i][j]= k
    
    # Termination
    v[len(state)-1][len(sentence)+1] = 0
    for i in range(1, len(state)):
        v_temp = v[i][len(sentence)]*transition_prob[state[i]][state[len(state)-1]]
        if v[len(state)-1][len(sentence)+1] < v_temp:
            v[len(state)-1][len(sentence)+1] = v_temp
            path[len(state)-1][len(sentence)+1] = i
    
    # Back tracking to determine the most probable path
    path_list = []
    i = path[len(state)-1][len(sentence)+1]
    path_list.append(state[i])
    for j in range(len(sentence),1,-1):
        i = path[i][j]
        path_list.append(state[i])
    path_list.reverse()
    return path_list 

print(viterbi(['This','is','a','sentence','.'], transition_prob, emission_prob, tag_set))
print(viterbi(['This','might','produce','a','result','if','the','system','works','well','.'], transition_prob, emission_prob, tag_set))
print(viterbi(['Can','a','can','can','a','can','?'], transition_prob, emission_prob, tag_set))
print(viterbi(['Can','a','can','move','a','can','?'], transition_prob, emission_prob, tag_set))
print(viterbi(['Can','you','walk','the','walk','and','talk','the','talk','?'], transition_prob, emission_prob, tag_set))