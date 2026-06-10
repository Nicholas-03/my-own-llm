import random

class Word_embedding:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.tokens = {}
    
    def embed_tokens(self, tokens):
        for token in tokens:
            self.get_word_position(token)
    
    def get_word_position(self, token):
        if token not in self.tokens:
            self.tokens[token] = [0.0] * self.dimensions
            self.add_random_weights(token)
            
        return self.tokens[token]
            
    def add_random_weights(self, token):
        for i in range(len(self.tokens[token])):
            self.tokens[token][i] = random.uniform(-1, 1)