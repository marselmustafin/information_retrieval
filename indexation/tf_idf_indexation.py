from pymorphy2 import MorphAnalyzer
from collections import defaultdict
from math import log
import numpy as np
import os

NORMALIZED_DOCS_PATH = "docs/normalized/"
INDEX_PATH = "indexation/"
INDEX_FILE_NAME = "tf_idf_index.txt"
morph = MorphAnalyzer()

docs_list = os.listdir(NORMALIZED_DOCS_PATH)

# Key: token, Value: count of appearings of this token for each doc
token_appearings = defaultdict(lambda: [0] * len(docs_list))

for filename in docs_list:
    with open(NORMALIZED_DOCS_PATH + filename, "r") as file:
        doc_index = int(filename.split(".")[0]) - 1
        tokens = file.read().strip().split("\t")
        for token in tokens:
            token_appearings[token][doc_index] += 1

# Sums of words for each doc
docs_tokens_sums = np.sum(list(token_appearings.values()), axis=0)

tfidfs = defaultdict(lambda: [0] * len(docs_list))
idfs = {}

for token in token_appearings.keys():
    idf = log(len(docs_list) / np.count_nonzero(token_appearings[token]))
    idfs[token] = idf
    for doc_index in range(len(docs_list)):
        tf = token_appearings[token][doc_index] / docs_tokens_sums[doc_index]
        tfidfs[token][doc_index] = tf * idf

# Index is saved in following format: WORD IDF ...TF_IDF_VALUES...
with open(INDEX_PATH + INDEX_FILE_NAME, "w") as result_file:
    for token, tfidfs in sorted(tfidfs.items()):
        index_row = token + "\t" + str(idfs[token]) + "\t" \
            + " ".join([str(tfidf) for tfidf in tfidfs])
        result_file.write(index_row + "\n")
