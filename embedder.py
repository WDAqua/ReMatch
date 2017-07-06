# Embedder (Glove wrapper)
# embeddings of two or more string longs are concatenated

# ===== imports =====
from glove import Glove
import numpy as np

# ===== definitions =====
class Embedder:
    
    # attributes
    gloveModel = None
    
    # constructor
    def __init__(self,path ='glove.6B.50d.txt'):
        self.gloveModel = Glove.load_stanford(path)
        print('Done loading GloVe model')
        
    # methods
    def getVector(self,word, method='concat'):
        if len(word.split()) == 1:
            if not self.gloveModel.dictionary.has_key(word.lower()):
                return None# doesn't exists
            index = self.gloveModel.dictionary[word.lower()]
            return self.gloveModel.word_vectors[index]
        elif method == 'concat' : # more than one
            bigVector = np.array([])
            for w in word.split():
                v = self.getVector(w,method)
                if v is None:
                    continue
                if len(bigVector) > 0:
                    bigVector = np.concatenate([bigVector,v])
                else:
                    bigVector = v
            return bigVector
        else : # do summation
            result = np.asarray([])
            for w in word.split():
                v = self.getVector(w,method)
                result = result+v
            return result
    
# ===== main testing =====          
if __name__ == "__main__":
    embedder = Embedder('../glove.6B.50d.txt')
    question = 'Hello yaser you are the man'
    print(embedder.getVector(question))