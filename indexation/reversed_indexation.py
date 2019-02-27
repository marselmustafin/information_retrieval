from pymorphy2 import MorphAnalyzer
import os

NORMALIZED_DOCS_PATH = "docs/normalized/"
INDEX_PATH = "indexation/"
INDEX_FILE_NAME = "reversed_index.txt"
morph = MorphAnalyzer()

docs_list = os.listdir(NORMALIZED_DOCS_PATH)

index = {}

for filename in docs_list:
    with open(NORMALIZED_DOCS_PATH + filename, "r") as file:
        doc_num = int(filename.split(".")[0])
        tokens = file.read().split("\t")
        for token in tokens:
            if token not in index:
                index[token] = ["0"] * len(docs_list)

            index[token][doc_num - 1] = "1"

with open(INDEX_PATH + INDEX_FILE_NAME, "w") as result_file:
    for token in index.keys():
        index_row = token + "\t" + " ".join(index[token]) + "\n"
        result_file.write(index_row)
