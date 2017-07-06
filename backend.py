# backend worker and embedder

# ===== imports =====
from reader import PattyReader
from embedder import Embedder
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ===== definitions =====
def processPattyData(pattyPath='dbpedia-relation-paraphrases_json.txt',glovePath='../glove.6B.50d.txt' ):
    patty = PattyReader(path=pattyPath)
    glove = Embedder(path =glovePath)
    patty.processData()
    #keys = patty.patterns.keys()
    mat = []
    key = 0
    for label,patterns in patty.patterns.iteritems():
        for pattern in patterns:
            #print(pattern)
            v = glove.getVector(pattern)
            v = np.append(v,key)
            mat.append(v)
        key = key +1
    #mat = np.asarray(mat)
    return mat, glove

def pad(A, length):
    arr = np.zeros(length)
    arr[:len(A)] = A
    return arr

def padVectors(mat, length=None):
    maxLength = max(len(vector) for vector in mat) if length is None else maxLength = length
    maxLength = maxLength - 1
    newMat = []
    for vector in mat:
        v = pad(vector[:-1],maxLength)
        newMat.append(np.append(v,vector[-1]))
    return newMat, maxLength

def calculateSimilarity(mat,vects):
    return cosine_similarity(mat,vects)

# ===== main testing =====          
if __name__ == "__main__":
    mat, _ = processPattyData()
    mat, maxLength = padVectors(mat)
    #calculateSimilarity(mat,padVectors())