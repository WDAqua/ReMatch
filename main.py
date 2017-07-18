# main file

# ===== imports =====
from __future__ import print_function
import frontend
import backend
import numpy as np
import JsonQueryParser as qald
import cPickle  as pickle

# ======= consts =============

''' number of winner relations for each part of the question '''
NUM_WINNERS = 10

''' minimum length of combinatorials of the question'''
MIN_LENGTH_COMP = 2

''' maximum length of combinatorials of the question'''
MAX_LENGTH_COMP = 3

# ===== definitions =====

def readQuestion():
    return 'Who is the wife of Obama'
    #return 'as president'
    #return 'wife of'
    #return 'To whom Barack Obama is married to'
    #return 'On which team does Ronaldo plays'
    #return 'With which team did Ronaldo plays ten games for'
    #return 'In which country was Beethoven born'
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

def processPatty():
    mat, glove, patty = backend.processPattyData()#,pattyPath='yago-relation-paraphrases_json.txt')#glovePath='C:/Users/Yaser/Desktop/glove.twitter.27B.25d.txt')
    mat, maxLength = backend.padVectors(mat)
    np.asarray(mat).dump('mat.dat')
    np.asarray(maxLength).dump('maxLength.dat')
    save_data(glove,'glove.dat')
    save_data(patty,'patty.dat')
    return mat, maxLength, glove, patty

def processQuestion(glove, maxLength, patty, mat,question):
    vectors, parts, pos, gen_question = frontend.processQuestion(glove,question,minLen=MIN_LENGTH_COMP,maxLen=MAX_LENGTH_COMP)
    vectors, _ = backend.padVectors(vectors,maxLength)
    similarities = backend.calculateSimilarity(np.array(vectors),np.array(mat)[:,:-1])
    winnersNum = NUM_WINNERS
    finalCountUnweighted = {}
    for sim in similarities:
        for index in np.argpartition(sim,-winnersNum)[-winnersNum:]:
            #print('winner',index)
            winner = patty.patterns.keys()[int(mat[index][-1])]
            if  finalCountUnweighted.has_key(winner):
                finalCountUnweighted[winner] += 1  
            else:
                finalCountUnweighted[winner] = 1
    finalCountWeighted = finalCountUnweighted.copy()
    for relation in finalCountWeighted:
        finalCountWeighted[relation] *= patty.weights[relation]
    finalCountWeightedSorted = sorted(finalCountWeighted.items(), key=lambda x:x[1], reverse=True)
    #print('done processing')
    return vectors, parts, pos, gen_question, similarities, finalCountUnweighted, finalCountWeighted, finalCountWeightedSorted

# ===== main testing =====          
if __name__ == "__main__":
    #mat, maxLength, glove, patty = processPatty()
    mat=np.load('mat.dat')
    maxLength=np.load('maxLength.dat')
    glove = load_data('glove.dat')
    patty = load_data('patty.dat')
    patty.processData()
    print('Hello')
    #vectors, parts, pos, gen_question, similarities, unweighted, weighted, result = processQuestion(glove,maxLength, patty, mat, readQuestion())
    '''questionsDatabase = qald.QueryDataBase('qald-7-train-multilingual.json')
    questions = questionsDatabase.openFile()
    questionsDatabase.createDataBase(questions)
    f = open('results.txt', 'w')
    for question in questionsDatabase.database.keys():
        try:
            print(question)
            vectors, parts, pos, gen_question, similarities, unweighted, weighted, result = processQuestion(glove,maxLength, patty, mat, question)
            f.write('\r\n===========================\r\n')
            f.write(question)
            f.write('\r\n')
            f.write(','.join(np.array(result[:10])[:,0]))
        except:
            continue
    f.close()'''
