from sentence_transformers import SentenceTransformer, util
import nltk
import numpy as np
import streamlit as st

MODEL_PATH = "multi-qa-MiniLM-L6-cos-v1"

class EmbeddingModel():
    '''
    This is an implementation of the EmbeddingModel class where we map the context provided into 
    word vectors using a Sentence Transformer

    This class also contains a method to get the closest chunk of text to a query
    '''

    def __init__(self,path = MODEL_PATH):
        self.model = SentenceTransformer(MODEL_PATH)
        nltk.download('punkt',quiet = True)
    
    def load_data(self,context):
        self.sentences = nltk.sent_tokenize(context)
        self.context = context
    
    def word_count(self,sentence):
        return len(nltk.word_tokenize(sentence))

    def create_mappings(self,MAX_LENGTH = 120):
        chunks = []
        curr_count = 0
        chunk = []
        for sentence in self.sentences:
            word_c = self.word_count(sentence)
            curr_count += word_c
            if curr_count < MAX_LENGTH:
                chunk.append(sentence)
            else:
                curr_count = 0
                chunks.append(' '.join(chunk))
                chunk = []
        if chunk:
            chunks.append(' '.join(chunk))
        self.chunks = chunks
        mapping = {}
        for i,chunk in enumerate(chunks):
            embeddings = self.model.encode(chunk)
            mapping[i] = embeddings
        self.mapping = mapping
        return 
    
    def get_closest(self, query):
        q_embedding = self.model.encode(query)
        HIGHEST = 0
        index = -1
        for k,v in self.mapping.items():
            dot_product = np.dot(q_embedding, v)
            if dot_product > HIGHEST:
                HIGHEST = dot_product
                index = k
        return self.chunks[index]

    