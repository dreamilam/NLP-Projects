#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

grammar = {
    ('S','NP','VP'):0.9,
    ('S','VP'):0.1,
    ('VP','V','NP'):0.5,
    ('VP','V'):0.1,
    ('VP','V','@VP_V'):0.3,
    ('VP','V','PP'):0.1,
    ('@VP_V','NP','PP'):1.0,
    ('NP','NP','NP'):0.1,
    ('NP','NP','PP'):0.2,
    ('NP','N'):0.7,
    ('PP','P','NP'):1.0,
    ('N','people'):0.5,
    ('N','fish'):0.2,
    ('N','tanks'):0.2,
    ('N','rods'):0.1,
    ('V','people'):0.1,
    ('V','fish'):0.6,
    ('V','tanks'):0.3,
    ('P','with'):1.0
}

def CKY(words, grammar):
    num_words = len(words)

    # Creating the list  of non terminals
    non_terminals = set()
    for key in grammar:
        non_terminals.add(key[0])
    nonterms = list(non_terminals)
    score = np.zeros((num_words, num_words+1, len(nonterms)))
    
    # Single word case
    for i in range(0, num_words):
        for A in nonterms:
            if (A,words[i]) in grammar:
                score[i][i+1][nonterms.index(A)] = grammar[(A, words[i])]
      
        # handle unaries
        added = True
        while added:
            added = False
            for A in nonterms: 
                for B in nonterms:
                    if score[i][i+1][nonterms.index(B)] > 0 and (A, B) in grammar:
                        prob = grammar[(A, B)] * score[i][i+1][nonterms.index(B)]
                        if prob > score[i][i+1][nonterms.index(A)]:
                            score[i][i+1][nonterms.index(A)] = prob
                            added = True
     

    # Main CKY loop
    for span in range(2, num_words+1):
        for begin in range(0, num_words - span + 1):
            end = begin + span
            for split in range(begin+1, end):
                for A in nonterms:
                    for B in nonterms:
                        for C in nonterms:
                            prob = score[begin][split][nonterms.index(B)] * score[split][end][nonterms.index(C)] * grammar.get((A, B, C), 0)
                            if prob > score[begin][end][nonterms.index(A)]:
                                score[begin][end][nonterms.index(A)] = prob
                
                # handle unaries
                added = True
                while added:
                    added = False
                    for A in nonterms:
                        for B in nonterms:
                            prob = grammar.get((A, B),0) * score[begin][end][nonterms.index(B)]
                            if prob > score[begin][end][nonterms.index(A)]:
                                score[begin][end][nonterms.index(A)] = prob
                                added = True
    
    return score[0][num_words][nonterms.index('S')] # Prob associated with 'S' in the top grid cell

print(CKY(['fish','people','fish','tanks'], grammar))
print(CKY(['people','with','fish','rods','fish','people'], grammar))
print(CKY(['fish','with','fish','fish'], grammar))
print(CKY(['fish','with','tanks','people','fish'], grammar))
print(CKY(['fish','people','with','tanks','fish','people','with','tanks'], grammar))
print(CKY(['fish','fish','fish','fish','fish'], grammar))
print(CKY(['rods','rods','rods','rods'], grammar))