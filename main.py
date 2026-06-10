import os
from src.tokenizer import Tokenizer
from src.word_embedding import Word_embedding
from src.positional_embedding import Positional_embedding
from src.utils import Utils

dimension = os.environ['dimension'] or 16
datasets_path = "datasets"

def main():
    utils = Utils()
    tokenizer = Tokenizer()
    word_embedding = Word_embedding(dimension)
    positional_embedding = Positional_embedding(dimension)
    
    # Load file
    text = utils.load_one_file(datasets_path)
    
    # Tokenize
    tokens = tokenizer.tokenize_text(text)
    
    # Meaning embedding
    word_embedding.embed_tokens(tokens)
    
    # Position embedding
    positional_embedding.embed_tokens(tokens)
    
    embedding = word_embedding.embed_tokens + positional_embedding.embedding
    