# question splitter

# ===== imports =====
import numpy as np
import itertools

# ===== definitions =====
class Splitter:
    
    # methods
    def __old_split__(self,question):
        words = question.split()
        combinations = [w for w in words]
        for i in range(len(words)-1):
            combinations.append(words[i]+' '+words[i+1])
        for i in range(len(words)-2):
            combinations.append(words[i]+' '+words[i+1]+' '+words[i+2])
        return combinations
    
    def split(self,question,method='regular',min=1,max=3):
        result = []
        words = question.split()
        if method == 'regular':
            combinations = np.array([words[start:end+1] 
                     for start in xrange(len(words)) 
                     for end in xrange(start, len(words))])
        else:
            combinations =[]
            for i in xrange(1,len(words)):
                combinations+=list(itertools.combinations(words,i))
            combinations = np.array(combinations)
        filter = np.array([len(x)>=min and len(x)<=max  for x in combinations])
        for comb in combinations[filter]:
            result.append(' '.join(comb))
        return np.array(result)
        
            
    def generalize(self, question, pos_tags):
        question = question.replace("'"," ").replace('?','').replace('.','').replace('!','')
        words = question.split()
        for pos in pos_tags:
            if pos[1] == 'NNP' or pos[1] == 'NNPS':
                words = ['' if w == pos[0] else w for w in words]
                #generalized_question = generalized_question.replace(pos[0],'') # remove noun
            if pos[1] == 'DT':
                words = ['determiner' if w == pos[0] else w for w in words]
                #generalized_question = generalized_question.replace(pos[0],'determiner')
            if pos[1] == 'JJ' or pos[1] == 'JJR' or pos[1] == 'JJS':
                words = ['adjective' if w == pos[0] else w for w in words]
                #generalized_question = generalized_question.replace(pos[0],'adjective')
            if pos[1] == 'CD':
                words = ['number' if w == pos[0] else w for w in words]
                #generalized_question = generalized_question.replace(pos[0],'number')
            if pos[1] == 'PRP' or pos[1] == 'PRP$' :#or pos[1] == 'WP' :
                words = ['pronoun' if w == pos[0] else w for w in words]
                #generalized_question = generalized_question.replace(pos[0],'pronoun')
            if pos[1] == 'CC':
                words = ['conjunction' if w == pos[0] else w for w in words]
                #generalized_question = generalized_question.replace(pos[0],'conjunction')
            if pos[1] == 'MD':
                words = ['modal' if w == pos[0] else w for w in words]
                #generalized_question = generalized_question.replace(pos[0],'modal')
            #if pos[1] == 'IN':
            #    generalized_question = generalized_question.replace(pos[0],'preposition')              
        return ' '.join(words)
            
# ===== main testing =====          
if __name__ == "__main__":
    splitter = Splitter()
    question = 'Hello yaser you are the man'
    print(splitter.split(question))