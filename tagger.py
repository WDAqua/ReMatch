# tagger do pos tagging of the question

# ===== imports =====
from practnlptools.tools import Annotator
import nltk

# ===== definitions =====
class POSTagger:
    
    # attributes
    annotator = None
    
    # constructor
    def __init__(self):
        self.annotator = Annotator()
   
    # methods
    def parse_old(self,question):
        annotator=Annotator()
        return annotator.getAnnotations(question, dep_parse=False)['pos']
    
    def parse(self,question):
        tokens = nltk.word_tokenize(question)
        return nltk.pos_tag(tokens)
    
# ===== main testing =====          
if __name__ == "__main__":
    tagger = POSTagger()
    question = 'Hello yaser you are the man'
    print(tagger.parse(question))