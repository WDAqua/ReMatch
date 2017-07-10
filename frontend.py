# frontend processing of question

# ===== imports =====
from splitter import Splitter
from tagger import POSTagger
from embedder import Embedder
from pprint import pprint as pp

# ===== definitions =====
def processQuestion(gloveModel, question, minLen=1,maxLen=3, vectorMethod='concat'):
    tagger = POSTagger()
    pos = tagger.parse(question)
    # create splitter and generalizer
    splitter = Splitter()
    gen_question = splitter.generalize(question, pos)
    parts = list(splitter.split(gen_question,min=minLen,max=maxLen))
    # create embedder part
    vectors = []
    for part in parts:
        vectors.append(gloveModel.getVector(part,method=vectorMethod))
    return vectors,parts,pos,gen_question

# ===== main testing =====          
if __name__ == "__main__":
    pp(processQuestion(Embedder('../glove.6B.50d.txt'),'Who is the wife of Barack Obama'))