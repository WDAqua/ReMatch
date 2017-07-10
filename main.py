# main file

# ===== imports =====
import frontend
import backend
import numpy as np




# ===== definitions =====

def readQuestion():
    #return 'Who is the wife of Obama'
    #return 'as president'
    #return 'wife of'
    #return 'To whom Barack Obama is married to'
    #return 'On which team does Ronaldo plays'
    #return 'With which team did Ronaldo plays ten games for'
    return 'In which country was Beethoven born'
    #return raw_input("Please enter a question: ")

def processPatty(vectorMethod):
    mat, glove, patty = backend.processPattyData(vectorMethod=vectorMethod,glovePath='C:/Users/Yaser/Desktop/glove.6B.100d.txt')#, pattyPath='yago-relation-paraphrases_json.txt')#glovePath='C:/Users/Yaser/Desktop/glove.twitter.27B.25d.txt')#pattyPath='yago-relation-paraphrases_json.txt'
    mat, maxLength = backend.padVectors(mat)
    return mat, maxLength, glove, patty

def processQuestion(glove, maxLength, patty, mat, vectorMethod):
    vectors, parts, pos, gen_question = frontend.processQuestion(glove,readQuestion(),minLen=1,maxLen=4, vectorMethod=vectorMethod)
    vectors, _ = backend.padVectors(vectors,maxLength)
    similarities = backend.calculateSimilarity(np.array(vectors),np.array(mat)[:,:-1])
    winnersNum = 2
    finalCount = {}
    for sim in similarities:
        #index = max(xrange(len(sim)), key = lambda x: sim[x])
        indexes = np.argpartition(sim,-winnersNum)[-winnersNum:]
        for index in indexes:
            winner = patty.patterns.keys()[int(mat[index][-1])]
            if  finalCount.has_key(winner):
                finalCount[winner] += 1  
            else:
                finalCount[winner] = 1
    print('done processing')
    return vectors, parts, pos, gen_question, similarities, finalCount

# ===== main testing =====          
if __name__ == "__main__":
    mat, maxLength, glove, patty = processPatty(vectorMethod='sum')
    vectors, parts, pos, gen_question, similarities, finalCount = processQuestion(glove,maxLength, patty, mat, vectorMethod='sum')
        
# Who is the wife of Obama