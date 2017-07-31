# Patty reader

# ===== imports =====
from pprint import pprint as pp
import utils

# ===== definitions =====
class PattyReader:
    
    # attributes
    content = []
    patterns = {}
    weights = {}
    
    # constructor
    def __init__(self,path):
        with open(path) as f:
            self.content = f.readlines()
        self.content = [x.strip() for x in self.content] 
    
    # methods
    def processData(self):
        # remove first
        for line in self.content[1:]:
            parts = line.split('\t')
            relation = parts[0]
            pattern = parts[1]
            # process pattern
            pattern = self.__fix_pattern__(pattern)
            if not self.patterns.has_key(parts[0]):
                self.patterns[relation] = []# [self.__make_relation_as_pattern__(relation)]
            self.patterns[relation].append(pattern) 
        totalCount = float(len(self.content)-1)
        for relation in self.patterns:
            count = len(self.patterns[relation])
            self.weights[relation] = 1. -  count/totalCount
                
    def printPreview(self):
        pp(self.patterns.items()[0:2])
        
    def __make_relation_as_pattern__(self,relation):
        return utils.splitCamelCase(relation)
      
    # private methods
    def __fix_pattern__(self,pattern):
        return pattern.replace(';','')\
            .replace('[[det]]','determiner')\
            .replace('[[pro]]','pronoun')\
            .replace('[[adj]]','adjective')\
            .replace('[[num]]','number')\
            .replace('[[con]]','conjunction')\
            .replace('[[prp]]','preposition')\
            .replace('[[mod]]','modal')

# ===== main testing =====          
if __name__ == "__main__":
    path = 'dbpedia-relation-paraphrases_json.txt'
    reader = PattyReader(path)
    reader.processData()
    reader.printPreview()