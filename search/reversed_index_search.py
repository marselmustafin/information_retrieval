from pymorphy2 import MorphAnalyzer
import argparse
import numpy as np
import sys

INDEX_FILE = "indexation/reversed_index.txt"
DOCS_LINKS_FILE = "index.txt"

doc_links = None

with open(DOCS_LINKS_FILE, "r") as file:
    doc_links = file.read().split()

parser = argparse.ArgumentParser(description='Reversed index search')
parser.add_argument('query', type=str, help='Search query')
args = parser.parse_args()

morph = MorphAnalyzer()

index = {}

with open(INDEX_FILE) as file:
    rows = file.readlines()
    for row in rows:
        token_presences = row.split("\t")
        token = token_presences[0]
        presences = token_presences[1]
        index[token] = [True if x == "1" else False
                        for x in presences.split(" ")]

keywords = args.query.strip().split()
normalized_keywords = [morph.parse(keyword)[0].normal_form
                       for keyword in keywords]

keywords_presences = []

for kw in normalized_keywords:
    if not index.get(kw, None):
        sys.exit("No results")

    keywords_presences.append(index[kw])

bitwised_presences = keywords_presences[0]

if len(keywords_presences) > 1:
    bitwised_presences = np.bitwise_and.reduce(keywords_presences)

for doc_index, bitwised_value in enumerate(bitwised_presences):
    print(doc_links[doc_index]) if bitwised_value else next
