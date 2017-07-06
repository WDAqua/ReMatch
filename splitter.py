# question splitter

# ===== imports =====

# ===== definitions =====
class Splitter:
    
    # methods
    def split(self,question):
        words = question.split()
        combinations = [w for w in words]
        for i in range(len(words)-1):
            combinations.append(words[i]+' '+words[i+1])
        for i in range(len(words)-2):
            combinations.append(words[i]+' '+words[i+1]+' '+words[i+2])
        return combinations
            
    def generalize(self, question, pos_tags):
        generalized_question = question
        for pos in pos_tags:
            if pos[1] == 'NNP':
                generalized_question = generalized_question.replace(pos[0],'noun')
            if pos[1] == 'DT':
                generalized_question = generalized_question.replace(pos[0],'determiner')
            if pos[1] == 'JJ' or pos[1] == 'JJR' or pos[1] == 'JJS':
                generalized_question = generalized_question.replace(pos[0],'adjective')
            if pos[1] == 'CD':
                generalized_question = generalized_question.replace(pos[0],'number')
            if pos[1] == 'PRP' or pos[1] == 'PRP$' or pos[1] == 'WP' :
                generalized_question = generalized_question.replace(pos[0],'pronoun')
            if pos[1] == 'CC':
                generalized_question = generalized_question.replace(pos[0],'conjunction')
            if pos[1] == 'MD':
                generalized_question = generalized_question.replace(pos[0],'modal')              
        return generalized_question
            
# ===== main testing =====          
if __name__ == "__main__":
    splitter = Splitter()
    question = 'Hello yaser you are the man'
    print(splitter.split(question))