# main file

# ===== imports =====
from __future__ import print_function
import frontend
import backend
import utils
import numpy as np
import JsonQueryParser as qald
import cPickle  as pickle
from distance import levenshtein as dist
import csv

# ======= consts =============

''' number of winner relations for each part of the question '''
NUM_WINNERS = 35

''' minimum length of combinatorials of the question'''
MIN_LENGTH_COMP = 2

''' maximum length of combinatorials of the question'''
MAX_LENGTH_COMP = 3

''' threshold for taking winners '''
THRESHOLD = 0.6

''' apply the penitly style '''
APPLY_PENILTY = True

''' use text razor api to get relations '''
USE_TEXT_RAZOR = True

''' apply the synonyms style '''
USE_SYNONYMS = False


# ===== definitions =====

def readQuestion():
    #return 'Who is the wife of Obama'
    #return 'as president'
    #return 'child of'
    #return 'To whom Barack Obama is married to'
    #return 'On which team does Ronaldo plays'
    #return 'With which team did Ronaldo plays ten games for'
    #return 'In which country was Beethoven born'
    #return 'which river flows through Bonn'
    #return 'Give me all actors who were born in Paris after 1950.'
    #return 'where in France is sparkling Wine produced'
    #return 'who was named as president of the USA'
    #return 'In which city are the headquarters of the United Nations?'
    return 'when was albert einstein born'
    #return raw_input("Please enter a question: ")
    
def load_data(filePath):
    try:
        with open(filePath) as f:
            x = pickle.load(f)
    except:
        x = []
    return x

def save_data(data,filePath):
    with open(filePath, "wb") as f:
        pickle.dump(data, f)
        
def calcDistance(label,relations):
    minValue = 9999999
    minString = None
    for relation in relations:
        #distance = dist(label,relation)
        distance = utils.dist_all_synsets(label,relation)
        if distance < minValue:
            minValue = distance
            minString = relation
    return minString,minValue

def processPatty():
    mat, glove, patty = backend.processPattyData()#glovePath="../glove.6B.50d.txt",pattyPath='yago-relation-paraphrases_json.txt')
    mat, maxLength = backend.padVectors(mat)
    np.asarray(mat).dump('mat.dat')
    np.asarray(maxLength).dump('maxLength.dat')
    save_data(glove,'glove.dat')
    save_data(patty,'patty.dat')
    return mat, maxLength, glove, patty

def processQuestion(glove, maxLength, patty, mat,question, benchmarking=False):
    vectors, parts, pos, gen_question, labels, apiResults = frontend.processQuestion(glove,question,minLen=MIN_LENGTH_COMP,maxLen=MAX_LENGTH_COMP,useAPI=USE_TEXT_RAZOR,useSynonyms=False)
    #vectors, _ = backend.padVectors(vectors,maxLength)
    similarities = backend.calculateSimilarity(np.array(vectors),np.array(mat)[:,:-1])
    winnersNum = NUM_WINNERS
    finalCountUnweighted = {}
    for sim in similarities:
        values = list(set(sim))
        #values = np.partition(list(set(sim)),kth=-winnersNum)[-winnersNum:]
        values= [v for v in values if v >= (THRESHOLD-0.1)]    
        values = sorted(values,reverse=True)[:winnersNum]
        indexes = []
        for value in values:
            for val in np.where(sim == value)[0]:
                indexes.append(val)
        for index in np.array(indexes).flatten():
            winner = patty.patterns.keys()[int(mat[index][-1])]
            if  finalCountUnweighted.has_key(winner):
                finalCountUnweighted[winner] += 1  
            else:
                finalCountUnweighted[winner] = 1
    finalCountWeighted = finalCountUnweighted.copy()
    if APPLY_PENILTY:
        for relation in finalCountWeighted:
            finalCountWeighted[relation] *= patty.weights[relation]
    finalCountWeightedSorted = sorted(finalCountWeighted.items(), key=lambda x:x[1], reverse=True)
    ''' apply the new second iteration '''
    relations = [x[0] for x in finalCountWeightedSorted]
    #print('relations: ',relations)
    splittedRelations = utils.splitCamelCase(relations)
    splittedRelations = utils.stripDownExtraWords(splittedRelations)
    newRelations = [utils.makeRelation(r) for r in splittedRelations]
    #splittedRelations = utils.stripDownExtraWords(relations)
    #patternsEmbeddings = [glove.getVector(p) for p in splittedRelations]
    #partsEmbeddings = []
    #finalCountUnweighted = {}
    for part in utils.stripDownExtraWords(parts):
        if not len(part) == 0:
            #print('part:', part)
            winner,d = calcDistance(part, newRelations)
            #print('winner: ', winner)
            if not benchmarking:
                if d > 4L:
                    continue
            if finalCountUnweighted.has_key(winner):
                finalCountUnweighted[winner]+=40
            else:
                finalCountUnweighted[winner]=40
            if USE_SYNONYMS:
                if len(part.split()) == 1:
                    syns = utils.stripDownExtraWords(utils.getSynonyms(part))
                    candidates = []
                    for syn in syns:
                        if not len(syn) == 0:
                            winner = calcDistance(syn, newRelations)
                            candidates.append(winner)
                    winner = sorted(candidates, key=lambda x:x[1])[0][0]
                    finalCountUnweighted[winner] += 40
        #if not len(part) == 0:
        #    partsEmbeddings.append(glove.getVector(part))
        #if len(part.split())==1:
        #    syns = utils.getSynonyms(part)
        #    for syn in syns[:3]:
        #        partsEmbeddings.append(glove.getVector(syn))
    #print("=========================================")
    finalCountWeighted = finalCountUnweighted.copy()
    if APPLY_PENILTY:
        for relation in finalCountWeighted:
            finalCountWeighted[relation] *= patty.weights[relation]
    finalCountWeightedSorted = sorted(finalCountWeighted.items(), key=lambda x:x[1], reverse=True)
    ''' end of second iteration '''
    return vectors, parts, pos, gen_question, similarities, finalCountUnweighted, finalCountWeighted, finalCountWeightedSorted, apiResults


# ===== main testing =====          
if __name__ == "__main__":
    mat, maxLength, glove, patty = processPatty()
    #mat=np.load('mat.dat')
    #maxLength=np.load('maxLength.dat')
    #glove = load_data('glove.dat')
    #patty = load_data('patty.dat')
    #patty.processData()
    #vectors, parts, pos, gen_question, similarities, unweighted, weighted, result = processQuestion(glove,maxLength, patty, mat, readQuestion())
