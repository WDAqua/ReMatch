# tagger do pos tagging of the question

# ===== imports =====
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import WordNetError
import re

# ===== definitions =====

def dist_all_synsets(first,second) : 
    f_syns = wn.synsets(first)
    
    s_syns = wn.synsets(second)
    
    #Path SImilarity
    #A 0-1 similarity score based on the shortest path that connects the senses in the is-a (hypernym/hypnoym) taxonomy.
    #A score of 1 represents identity i.e. comparing a sense with itself will return 1.
    least_sim = 0.0
    for f in f_syns :
        for s in s_syns :
            path_sim = wn.path_similarity(f,s)
            if path_sim > least_sim :
                least_sim = path_sim;
    return 1.-least_sim

def splitCamelCase(string):
    if type(string) is list:
        return [splitCamelCase(w) for w in string]
    return ' '.join(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', string)).lower()

def splitSnakeCase(string):
    return ' '.join(string.split('_'))

def makeRelation(string):
    if type(string) is list:
        string=' '.join(string)
    upper = string.title()
    words = upper.split()
    words[0]=words[0].lower()
    return ''.join(words)
    
def getSynonyms(word):
    if type(word) is list:
        return [getSynonyms(w) for w in word]
    syns = [x.lemma_names() for x in wn.synsets(word)]
    syns = list(set(reduce(lambda x,y: x+y,syns)))
    return [splitSnakeCase(s) for s in syns]

def stripDownExtraWords(orginalString):
    if type(orginalString) is list:
        return [stripDownExtraWords(string) for string in orginalString]
    toRemove = ['do', 'the', 'a', 'of', 'as', 'in', 'on', 'at', 'does', 'who', 'determiner','did',
                'pronoun', 'adjective', 'number', 'conjunction', 'preposition', 'modal','are', 'an',
                'whom', 'what', 'why', 'how', 'where', 'was', 'were', 'this', 'is', 'by', 'which',
                'for', 'has', 'have', 'all', 'often']
    words = orginalString.lower().split()
    exists = [x for x in words if x in toRemove]
    newWords = [x for x in words if x not in exists]
    return ' '.join(newWords)

# ===== main testing =====          
if __name__ == "__main__":
    #print(stripDownExtraWords(splitCamelCase(['thisIsNotANiceString','GoodFeeling','Holy moly'])))
    #print(getSynonyms('flows'))
    #print(makeRelation('yaser is great'))
    print(splitCamelCase('yaser'))