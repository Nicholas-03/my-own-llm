class Positional_embedding:
    def __init__(self, dimension):
        self.dimension = dimension
        self.embedding = {}
        
    def embed_tokens(self, tokens):
        return tokens