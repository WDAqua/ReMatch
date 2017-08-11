# ReMatch
K-Cap 2017 Project 
## Capturing Knowledge in Semantically-typed Relational Patterns to Enhance Relation Linking
Note: The evaluation results for K-Cap 2017 paper is in "Evaluation results" Folder.

## For Installation and Running

### Python Version
Python 2.7

### Required packages
* numpy
* glove_python
* sklearn
* practnlptool
* textrazor
* cPickle
* distance
* nltk
* SocketServer

### Required data files
* glove precomputed data files
  - download from (http://nlp.stanford.edu/data/glove.6B.zip) the default file used by the code is (glove.6B.50d.txt)
* patty data files (included <not big>)

### Required Data
* text-razor API key

## Code explanation:
PS. File names are self explanatory

1. Tagger: POS tagger
1. Splitter: split the question into combinations
1. Embedder: glove wrapper to convert question into vectors
1. Reader: PATTY data reader
1. Backend: the complete process of reading PATTY data and create embeddings, with the cosine similarity code
1. Frontend: the complete process of reading a question and processing it
1. Textrazor_Api: the API wrapper for the textrazor service
1. main: where the magic happens
1. api: for the web UI interface
1. webService: for calling the system as a web service locally

## Running local web service
Running the service via **./webService.py [port]**


and calling it is simple i.e. (http://localhost/question_url_encoded)
  - Response will look like this:
  ```
  {
   "result":[
      "result 1",
      "result 2", ...
   ],
   "parts":[
      "part 1",
      "part 2", ...
   ],
   "pos":[
      [
         "word",
         "pos tag"
      ], ...
   ],
   "gen_question":"generalized question here"
}
  ```


## Any other issues while running the code:
Please email to Yaser (yaser.jaradeh@uni-bonn.de) or Kuldeep (kskuldeepvit@gmail.com) if you face any problem.

