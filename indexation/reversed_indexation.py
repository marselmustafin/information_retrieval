from pymorphy2 import MorphAnalyzer
import os

NORMALIZED_DOCS_PATH = 'docs/normalized/'
INDEX_PATH = "indexation/"
INDEX_FILE_NAME = "reversed_index.txt"
morph = MorphAnalyzer()

docs_list = os.listdir(NORMALIZED_DOCS_PATH)
sorted_docs = sorted(docs_list, key=lambda d: int(d.split(".")[0]))

index = {}

for filename in sorted_docs:
    with open(NORMALIZED_DOCS_PATH + filename, "r") as file:
        doc_num = int(filename.split(".")[0])
        tokens = file.read().split("\t")
        for token in tokens:
            if token not in index:
                index[token] = [0] * len(docs_list)

            index[token][doc_num - 1] = 1

with open(INDEX_PATH + INDEX_FILE_NAME, "w") as result_file:
    for token in index.keys():
        index_row = "\t".join((token, " ".join(str(t) for t in index[token])))
        result_file.write(index_row + "\n")
