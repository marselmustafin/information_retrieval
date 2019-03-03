from pymorphy2 import MorphAnalyzer
import numpy as np
import os

NORMALIZED_DOCS_PATH = "docs/normalized/"
INDEX_PATH = "indexation/"
INDEX_FILE_NAME = "tf_idf_index.txt"
morph = MorphAnalyzer()

docs_list = os.listdir(NORMALIZED_DOCS_PATH)

# Key: token, Value: count of appearings of this token for each doc
token_appearings = {}

for filename in docs_list:
    with open(NORMALIZED_DOCS_PATH + filename, "r") as file:
        doc_index = int(filename.split(".")[0]) - 1
        tokens = file.read().split("\t")
        for token in tokens:
            token_appearings.setdefault(
                token, [0] * len(docs_list))[doc_index] += 1

# Sums of words for each doc
docs_words_sums = np.sum(list(token_appearings.values()), axis=0)

index = {}

for word in token_appearings.keys():
    for doc_index in range(len(docs_list)):
        tf = token_appearings[word][doc_index] / docs_words_sums[doc_index]
        idf = len(docs_list) / np.count_nonzero(token_appearings[word])

        index.setdefault(word, [0] * len(docs_list))[doc_index] = tf * idf

with open(INDEX_PATH + INDEX_FILE_NAME, "w") as result_file:
    for token, tfidfs in index.items():
        index_row = token + "\t" + " ".join([str(tfidf) for tfidf in tfidfs])
        result_file.write(index_row + "\n")
