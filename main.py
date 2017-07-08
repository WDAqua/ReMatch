# main file

# ===== imports =====
import frontend
import backend
import numpy as np

# ===== definitions =====

def readQuestion():
    return 'Who is the wife of Obama'
    #return raw_input("Please enter a question: ")

def processPatty():
    mat, glove, patty = backend.processPattyData()#pattyPath='yago-relation-paraphrases_json.txt')
    mat, maxLength = backend.padVectors(mat)
    return mat, maxLength, glove, patty

def processQuestion(glove, maxLength, patty):
    vectors, parts, pos, gen_question = frontend.processQuestion(glove,readQuestion(),minLen=3,maxLen=3)
    vectors, _ = backend.padVectors(vectors,maxLength)
    similarities = backend.calculateSimilarity(np.array(vectors),np.array(mat)[:,:-1])
    finalCount = {}
    for sim in similarities:
        index = max(xrange(len(sim)), key = lambda x: sim[x])
        winner = patty.patterns.keys()[int(mat[index][-1])]
        if  finalCount.has_key(winner):
            finalCount[winner] += 1  
        else:
            finalCount[winner] = 1
    print('done processing')
    return vectors, parts, pos, gen_question, similarities, finalCount

# ===== main testing =====          
if __name__ == "__main__":
    mat, maxLength, glove, patty = processPatty()
    vectors, parts, pos, gen_question, similarities, finalCount = processQuestion(glove,maxLength, patty)
        
# Who is the wife of Obama