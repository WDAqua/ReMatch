# main file

# ===== imports =====
from __future__ import print_function
import frontend
import backend
import numpy as np
import JsonQueryParser as qald
import cPickle  as pickle
from distance import levenshtein as dist

# ======= consts =============

''' number of winner relations for each part of the question '''
NUM_WINNERS = 25

''' minimum length of combinatorials of the question'''
MIN_LENGTH_COMP = 2

''' maximum length of combinatorials of the question'''
MAX_LENGTH_COMP = 3

''' apply the penitly style '''
APPLY_PENILTY = True

''' use text razor api to get relations '''
USE_TEXT_RAZOR = False

''' apply the synonyms style '''
USE_SYNONYMS = False

''' apply label comparison technique '''
USE_LABEL_COMPARESION = True

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
    return 'Who was the successor of John F. Kennedy?'
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
        distance = dist(label,relation)
        if distance < minValue:
            minValue = distance
            minString = relation
    return minString

def processPatty():
    mat, glove, patty = backend.processPattyData()#,pattyPath='yago-relation-paraphrases_json.txt')#glovePath='C:/Users/Yaser/Desktop/glove.twitter.27B.25d.txt')
    mat, maxLength = backend.padVectors(mat)
    np.asarray(mat).dump('mat.dat')
    np.asarray(maxLength).dump('maxLength.dat')
    save_data(glove,'glove.dat')
    save_data(patty,'patty.dat')
    return mat, maxLength, glove, patty

def processQuestion(glove, maxLength, patty, mat,question):
    vectors, parts, pos, gen_question, labels = frontend.processQuestion(glove,question,minLen=MIN_LENGTH_COMP,maxLen=MAX_LENGTH_COMP,useAPI=USE_TEXT_RAZOR,useSynonyms=USE_SYNONYMS)
    #vectors, _ = backend.padVectors(vectors,maxLength)
    if USE_LABEL_COMPARESION:
        for label in labels:
            if patty.patterns.has_key(label):
                print(label)
            #print(label,calcDistance(label,patty.patterns.keys()))
    similarities = backend.calculateSimilarity(np.array(vectors),np.array(mat)[:,:-1])
    winnersNum = NUM_WINNERS
    finalCountUnweighted = {}
    for sim in similarities:
        values = np.partition(list(set(sim)),kth=-winnersNum)[-winnersNum:]
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
    return vectors, parts, pos, gen_question, similarities, finalCountUnweighted, finalCountWeighted, finalCountWeightedSorted

# ===== main testing =====          
if __name__ == "__main__":
    #mat, maxLength, glove, patty = processPatty()
    mat=np.load('mat.dat')
    maxLength=np.load('maxLength.dat')
    glove = load_data('glove.dat')
    patty = load_data('patty.dat')
    patty.processData()
    vectors, parts, pos, gen_question, similarities, unweighted, weighted, result = processQuestion(glove,maxLength, patty, mat, readQuestion())
    questionsDatabase = qald.QueryDataBase('qald-7-train-multilingual.json')
    questions = questionsDatabase.openFile()
    questionsDatabase.createDataBase(questions)
    count=0
    matches=[]
    matches2=[]
    matches3=[]
    matches4=[]
    matches5=[]
    matches10=[]
    cf2=0.0
    cf3=0.0
    cf4=0.0
    cf5=0.0
    cf6=0.0
    cf7=0.0
    cf8=0.0
    cf9=0.0
    cf10=0.0
    for question in questionsDatabase.database.keys() :
        try:
            flag=False
            for relation in questionsDatabase.database[question] :
                if patty.patterns.has_key(relation):
                    flag=True
                    break
            if not flag:
                continue
            count+=1        
            _, _, _, _, _, _, _, finalCountWeightedSorted = processQuestion(glove,maxLength, patty, mat,question)
            results=[x[0] for x in finalCountWeightedSorted]
            match=[x for x in results[:1] if x in questionsDatabase.database[question]]
            match2=[x for x in results[:2] if x in questionsDatabase.database[question]]
            match3=[x for x in results[:3] if x in questionsDatabase.database[question]]
            match4=[x for x in results[:4] if x in questionsDatabase.database[question]]
            match5=[x for x in results[:5] if x in questionsDatabase.database[question]]
            match10=[x for x in results[:10] if x in questionsDatabase.database[question]]

            

            if len(match) > 0 :
                matches.append((match[0],results.index(match[0])))
            if len(match2) > 0 :
                for m in match2 :
                    matches2.append((m,results.index(m)))
            if len(match3) > 0 :
                for m in match3 :
                    matches3.append((m,results.index(m)))
            if len(match4) > 0 :
                for m in match4 :
                    matches4.append((m,results.index(m)))
            if len(match5) > 0 :
                for m in match5 :
                    matches5.append((m,results.index(m)))
            if len(match10) > 0 :
                for m in match10 :
                    matches10.append((m,results.index(m)))    
                    
                    
            match2=[x for x in [results[1]] if x in questionsDatabase.database[question]]
            if len(match2) > 0 :
                cf2+=0.5
            match3=[x for x in [results[2]] if x in questionsDatabase.database[question]]
            if len(match3) > 0 :
                cf3+=0.3
            match4=[x for x in [results[3]] if x in questionsDatabase.database[question]]
            if len(match4) > 0 :
                cf4+=0.25
            match5=[x for x in [results[4]] if x in questionsDatabase.database[question]]
            if len(match5) > 0 :
                cf5+=0.2
            match6=[x for x in [results[5]] if x in questionsDatabase.database[question]]
            if len(match6) > 0 :
                cf6+=1./6.
            match7=[x for x in [results[6]] if x in questionsDatabase.database[question]]
            if len(match7) > 0 :
                cf7+=1./7.
            match8=[x for x in [results[7]] if x in questionsDatabase.database[question]]
            if len(match8) > 0 :
                cf8+=1./8.
            match9=[x for x in [results[8]] if x in questionsDatabase.database[question]]
            if len(match9) > 0 :
                cf9+=1./9.
            match10=[x for x in [results[9]] if x in questionsDatabase.database[question]]
            if len(match10) > 0 :
                cf10+=0.1  
        except:
            continue
        
         
    cf=len(matches)
    cf2=cf2+cf
    cf3=cf3+cf2
    cf4=cf4+cf3
    cf5=cf5+cf4
    cf6=cf6+cf5
    cf7=cf7+cf6
    cf8=cf8+cf7
    cf9=cf9+cf8
    cf10=cf10+cf9
    
    pre=cf/float(count)
    pre2=cf2/float(count)
    pre3=cf3/float(count)
    pre4=cf4/float(count)
    pre5=cf5/float(count)
    pre10=cf10/float(count)
   

    re2=len(matches2)/float(count)
    re3=len(matches3)/float(count)
    re4=len(matches4)/float(count)
    re5=len(matches5)/float(count)
    re10=len(matches10)/float(count)
