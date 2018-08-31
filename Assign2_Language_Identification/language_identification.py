import math
classes = ['de', 'en', 'nl', 'sv']
texts = {}
alphabet = set()

count_unigram = {}    # Dictionary to store the counts of all unigrams present in the text of a particular language
count_bigram = {}     # Dictionary to store the counts of all bigrams present in the text of a particular language
probs={}              # Dictionary to store the probablitiy of a bigram appearing in a particular language

for lang in classes:
    texts[lang] = [line.strip() for line in open(lang,'r',encoding='utf-8')][0]
    alphabet |= {unigram for unigram in texts[lang]}

    # Get the unigram counts for all languages
    count_unigram[lang] = {}
    for unigram in texts[lang]:
        if unigram in count_unigram[lang]:
            count_unigram[lang][unigram] += 1
        else:
            count_unigram[lang][unigram] = 1

    # Get the bigram counts for all languages
    count_bigram[lang] = {}
    for i in range(0,len(texts[lang])-1):
        bigram = texts[lang][i:i+2]
        if bigram in count_bigram[lang]:
            count_bigram[lang][bigram] += 1
        else:
            count_bigram[lang][bigram] = 1

    # Calculate the probability of a bigram appearing in a language
    probs[lang] = {}
    for x in alphabet:
        for y in alphabet:
            probs[lang][x+y] = math.log((count_bigram[lang].get(x+y, 0) + 1)/ (count_unigram[lang].get(x, 0) + len(alphabet)))

# Function to classify a given string by summing up the bigram log probabilities
def classify(probs, classes, string):
    string = " " + string
    string_prob = {}
    max_prob = -math.inf
    max_prob_lang = ""
    for lang in classes:
        string_prob[lang] = 1
        for i in range(0, len(string)-1):
            string_prob[lang] += probs[lang].get(string[i:i+2],0)
        if(string_prob[lang] > max_prob):
            max_prob = string_prob[lang]
            max_prob_lang = lang
    return (max_prob_lang, string_prob)

print (classify(probs, classes, 'this is a very short text'))
print (classify(probs, classes, 'dies ist ein sehr kurzer text'))
print (classify(probs, classes, 'dit is een zeer korte tekst'))
print (classify(probs, classes, 'detta är en mycket kort text'))