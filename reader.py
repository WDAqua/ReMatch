# Patty reader

# ===== imports =====
from pprint import pprint as pp

# ===== definitions =====
class PattyReader:
    
    # attributes
    content = []
    patterns = {}
    
    # constructor
    def __init__(self,path):
        with open(path) as f:
            self.content = f.readlines()
        self.content = [x.strip() for x in self.content] 
    
    # methods
    def processData(self):
        self.content.pop() # remove first
        for line in self.content:
            parts = line.split('\t')
            relation = parts[0]
            pattern = parts[1]
            # process pattern
            pattern = self.__fix_pattern__(pattern)
            if self.patterns.has_key(parts[0]):
                self.patterns[relation].append(pattern) 
            else:
                self.patterns[relation] = [pattern]
                
    def printPreview(self):
        pp(self.patterns.items()[0:2])
      
    # private methods
    def __fix_pattern__(self,pattern):
        return pattern.replace(';','')\
            .replace('[[det]]','determiner')\
            .replace('[[pro]]','pronoun')\
            .replace('[[adj]]','adjective')\
            .replace('[[num]]','number')\
            .replace('[[con]]','conjunction')\
            .replace('[[prp]]','pronoun')\
            .replace('[[mod]]','modal')

# ===== main testing =====          
if __name__ == "__main__":
    path = 'dbpedia-relation-paraphrases_json.txt'
    reader = PattyReader(path)
    reader.processData()
    reader.printPreview()