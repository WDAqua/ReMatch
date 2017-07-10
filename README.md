# ReMatch
Semantic Lab project

## Installation and Running
### Required packages
* numpy
* glove_python
* sklearn
* practnlptool

### Required data files
* glove precomputed data files
* patty data files (included <not big>)

## Code explanation:
PS. File names are self explanatory

1. Tagger: POS tagger
1. Splitter: split the question into combinations
1. Embedder: glove wrapper to convert question into vectors
1. Reader: PATTY data reader
1. Backend: the complete process of reading PATTY data and create embeddings, with the cosine similarity code
1. Frontend: the complete process of reading a question and processing it
1. main: where the magic happens


## Any other issues:
Please try solving it before telling me :)

