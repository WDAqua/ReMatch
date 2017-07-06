# frontend processing of question

# ===== imports =====
from splitter import Splitter
from tagger import POSTagger
from embedder import Embedder
from pprint import pprint as pp

# ===== definitions =====
def processQuestion(gloveModel, question):
    tagger = POSTagger()
    pos = tagger.parse(question)
    # create splitter and generalizer
    splitter = Splitter()
    gen_question = splitter.generalize(question, pos)
    parts = splitter.split(gen_question)
    # create embedder part
    vectors = []
    for part in parts:
        vectors.append(gloveModel.getVector(part))
    return vectors,parts,pos,gen_question

# ===== main testing =====          
if __name__ == "__main__":
    pp(processQuestion(Embedder(),'Who is the wife of Barack Obama'))