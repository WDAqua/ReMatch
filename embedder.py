# Embedder (Glove wrapper)
# embeddings of two or more string longs are concatenated

# ===== imports =====
from glove import Glove
from urllib import urlopen
import numpy as np
import re
import json


# ===== definitions =====
class Embedder:
    
    # attributes
    gloveModel = None
    length = 50
    fixPatterns = False
    
    # constructor
    def __init__(self,path ='glove.6B.50d.txt', fixPatterns=False):
        self.gloveModel = Glove.load_stanford(path)
        self.length = int(re.findall('\.[0-9][0-9][0-9]?d',path)[0][1:-1])
        self.fixPatterns = fixPatterns
        #print('Done loading GloVe model')
        
    # methods
    def getVector(self, word):
        if len(word.split()) == 1:
            if not self.gloveModel.dictionary.has_key(word.lower()):
                if not self.fixPatterns:
                    word = self.__use_suggessions__(word)
                    if len(word.split()) == 1:
                        if not self.gloveModel.dictionary.has_key(word.lower()):
                            #print(word,'not found')
                            return np.zeros(self.length)
                    else:
                        return self.getVector(word)
                else:
                   #print(word,'not found')
                   return np.zeros(self.length) 
            index = self.gloveModel.dictionary[word.lower()]
            return self.gloveModel.word_vectors[index]
        else : # do summation
            result = np.array([])
            for w in word.split():
                v = self.getVector(w)
                if v is None:
                    continue
                if len(result) == 0:
                    result = np.zeros(self.length) 
                result = np.add(result,v)/2.
            return result
        
    def __use_suggessions__(self,phrase):
        url = "http://suggestqueries.google.com/complete/search?output=firefox&q="
        webpage = urlopen(url + phrase).read()
        try:
            jsonObj = json.loads(webpage)
        except ValueError:
            return phrase
        if len(jsonObj[1]) == 0:
            return phrase
        #print(jsonObj[1][0])
        return jsonObj[1][0]
    
# ===== main testing =====          
if __name__ == "__main__":
    embedder = Embedder('../glove.6B.50d.txt')
    question = 'Hello yaser you are the man'
    print(embedder.getVector(question))