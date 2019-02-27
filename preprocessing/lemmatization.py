from pymorphy2 import MorphAnalyzer
from nltk.tokenize.casual import TweetTokenizer
import os

RAW_DOCS_PATH = 'docs/raw/'
NORMALIZED_DOCS_PATH = 'docs/normalized/'
tokenizer = TweetTokenizer()
morph = MorphAnalyzer()

if not os.path.exists(NORMALIZED_DOCS_PATH):
    os.makedirs(os.path.dirname(NORMALIZED_DOCS_PATH))

for filename in os.listdir(RAW_DOCS_PATH):
    with open(RAW_DOCS_PATH + filename, "r") as file:
        tokens = tokenizer.tokenize(file.read())
        lemmas = [morph.parse(token)[0].normal_form for token in tokens]

    with open(NORMALIZED_DOCS_PATH + filename, "w") as f:
        f.write("\t".join(lemmas))
