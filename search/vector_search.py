from pymorphy2 import MorphAnalyzer
from collections import Counter
from numpy import linalg as la
from math import sqrt, log
import argparse
import numpy as np
import sys

INDEX_FILE = "indexation/tf_idf_index.txt"
DOCS_LINKS_FILE = "index.txt"
TOP_RESULTS_NUM = 10

with open(DOCS_LINKS_FILE, "r") as file:
    doc_links = file.read().split()

parser = argparse.ArgumentParser(description='Vector search')
parser.add_argument('query', type=str, help='Search query')
args = parser.parse_args()

morph = MorphAnalyzer()

keywords = args.query.strip().split()
normalized_keywords = [morph.parse(keyword)[0].normal_form
                       for keyword in keywords]

keywords_counts = Counter()

for keyword in normalized_keywords:
    keywords_counts[keyword] += 1

index = {}
idfs = {}

with open(INDEX_FILE) as file:
    for line in file.readlines():
        token, idf, weights = line.split("\t")
        idfs[token] = float(idf)
        index[token] = [float(x) for x in weights.split(" ")]

vocab = [*index]
t_index = np.array([*index.values()]).T

similarities = []

for doc_vec in t_index:
    squared_sum = 0
    multiplied_components_sum = 0
    doc_vec_norm = sqrt(sum([comp**2 for comp in doc_vec]))
    for token in set(normalized_keywords):
        if token not in vocab:
            continue

        token_vocab_index = vocab.index(token)
        token_tfdif = keywords_counts[token] / len(keywords) * idfs[token]

        multiplied_components_sum += token_tfdif * doc_vec[token_vocab_index]
        squared_sum += token_tfdif**2

    similarity = multiplied_components_sum / (doc_vec_norm * sqrt(squared_sum))
    similarities.append(similarity)

sorted_links = \
    sorted(zip(doc_links, similarities), key=lambda p: p[1], reverse=True)

for result, similarity_coef in sorted_links[0:TOP_RESULTS_NUM]:
    print(result + " " + str(similarity_coef) + "\n")
