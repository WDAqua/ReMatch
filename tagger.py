# tagger do pos tagging of the question

# ===== imports =====
from practnlptools.tools import Annotator

# ===== definitions =====
class POSTagger:
    
    # attributes
    annotator = None
    
    # constructor
    def __init__(self):
        self.annotator = Annotator()
   
    # methods
    def parse(self,question):
        annotator=Annotator()
        return annotator.getAnnotations(question, dep_parse=False)['pos']
    
    
    
# ===== main testing =====          
if __name__ == "__main__":
    tagger = POSTagger()
    question = 'Hello yaser you are the man'
    print(tagger.parse(question))