# ReMatch
Semantic Lab project

## components of the code


0. tagger : POS tagger
0. splitter : split the question into combinatorials and generalize question through POS tags
0. embedder : use glove to get the vectors representation and combine vectors togather
0. reader : read patty data and collect it in data structure and create vectors of embeddings for it
0. backend : process the patty data in the correct workflow of the process
0. frontend : parse the question and use tagging, splitting and embedding in the correct workflow
0. main: run everything (still under word)
