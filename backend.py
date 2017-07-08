# backend worker and embedder

# ===== imports =====
from reader import PattyReader
from embedder import Embedder
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial

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
    return mat, glove, patty

def pad(A, length):
    arr = np.zeros(length)
    arr[:len(A)] = A
    return arr

def padVectors(mat, length=None):
    if length is None:
        maxLength = max(len(vector) for vector in mat)
        maxLength = maxLength - 1
    else:
        maxLength = length
    newMat = []
    for vector in mat:
        v = pad(vector[:-1],maxLength)
        if length is None:
            v = np.append(v,vector[-1])
        newMat.append(v)
    return newMat, maxLength

def calculateSimilarity(vects,mat):
    '''
    result = []
    for vec in vects:
        similarities = []
        for pattern in mat:
            similarities.append(1-spatial.distance.cosine(vec,pattern))
        result.append(np.array(similarities))
    return result'''
    return cosine_similarity(vects,mat)

# ===== main testing =====          
if __name__ == "__main__":
    mat, _, _ = processPattyData()
    mat, maxLength = padVectors(mat)
    #calculateSimilarity(mat,padVectors())