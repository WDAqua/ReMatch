# ReMatch
K-Cap 2017 Project 
## Capturing Knowledge in Semantically-typed Relational Patterns to Enhance Relation Linking
Note: The evaluation results for K-Cap 2017 paper is in "Evaluation results" Folder.

## For Installation and Running
### Required packages
* numpy
* glove_python
* sklearn
* practnlptool
* textrazor
* cPickle
* distance
* nltk

### Required data files
* glove precomputed data files
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


## Any other issues while running the code:
Please email to Yaser (yaser.jaradeh@uni-bonn.de) or Kuldeep (kskuldeepvit@gmail.com) if you face any problem.

