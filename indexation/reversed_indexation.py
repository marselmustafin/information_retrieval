from pymorphy2 import MorphAnalyzer
from collections import defaultdict
import os

NORMALIZED_DOCS_PATH = "docs/normalized/"
INDEX_PATH = "indexation/"
INDEX_FILE_NAME = "reversed_index.txt"
morph = MorphAnalyzer()

docs_list = os.listdir(NORMALIZED_DOCS_PATH)

index = defaultdict(lambda: ["0"] * len(docs_list))

for filename in docs_list:
    with open(NORMALIZED_DOCS_PATH + filename, "r") as file:
        doc_index = int(filename.split(".")[0]) - 1
        tokens = file.read().strip().split("\t")
        for token in tokens:
            index[token][doc_index] = "1"

with open(INDEX_PATH + INDEX_FILE_NAME, "w") as result_file:
    for token, appearings in index.items():
        index_row = token + "\t" + " ".join(appearings) + "\n"
        result_file.write(index_row)
