from textrazor import TextRazor
from pprint import pprint as pp

#API_KEY = "04fd9a5a817266cc2912266cd152da35a25d08c95f9b5edefb94ed97"
#API_KEY = "9d0ac08f05f6f546d230e05f634efe26fc035479d130231dad4fd5cb"
API_KEY = "785231deddf38c8f5b8e73adfa9d3b3b6b3f6859e391c63b84786afc"
#API_KEY = "b8871f52ee4c442a6435ed7b142600c00fed4cccfcf2bc6747bb8cb0"
#API_KEY = "233a4d7450ba94588f67301490603aaa4c1d973f5cfdb2c445165a61"
#API_KEY = "875417a3adfb35e2b0c9d76e16bb92e1974547605e72d66c20f4b4ce"
#API_KEY = "2d3680ab6b46fa81ff6293ee6e924fcbdbe9658d61c107e17b4669b3"
#API_KEY = "6559f7ac589ff5f014e4c4058ba0531987a9a83e067427a2768a2fc9"
#API_KEY = "f0c1f18fbb833cc10a6dfe7295616e8d6120f1fd4180173e93d0c7a7"
#API_KEY = "fe1930d48b3b520da0b820cfa6ad01d26c8dd9d6c62a06f7dede09a0"
#API_KEY = "8ca44890eb757ac572861b40845e88e5fdb65d2894acc9cac9ac3d20"
#API_KEY = "803dc1c05746b1296d397a465f71f95e9cb89fcf98fc1e875bec7eb6"
#API_KEY = "8f8dbf8b93a96d12c178fd06c08be95af67c6c2e58e2e3650447d0c6"   
#API_KEY = "fee2861b8a669c3804ff0d00e39e9cbc1f8e96942ab6f9a082674535"


class RelationResult:
    def __init__(self, predicate_positions, predicate_words, property_positions, property_words):
      self.predicate_positions_ = predicate_positions
      self.predicate = predicate_words
      self.property_positions_ = property_positions
      self.property = property_words
      
    def __str__( self):
        return self.predicate+' --> '+self.property
    
    def __repr__(self):
        return self.__str__()
      
def getBinaryRelations(string,extractors=["words", "relations"]):
    client = TextRazor(API_KEY,extractors=extractors)
    response = client.analyze(string)
    result = []
    root = [w.token for w in response.words() if w.parent_position is None]
    for relation in response.relations():
        result.append(RelationResult(relation.predicate_positions,' '.join([w.token for w in relation.predicate_words]),[],''))
    for relation in response.properties():
        result.append(RelationResult(relation.predicate_positions,' '.join([w.token for w in relation.predicate_words]),relation.property_positions,' '.join([w.token for w in relation.property_words])))
    return result, root
        
if __name__ == "__main__":
    pp(getBinaryRelations(string='On which team does Ronaldo plays'))