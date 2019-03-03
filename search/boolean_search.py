from pymorphy2 import MorphAnalyzer
import argparse
import numpy as np
import sys

INDEX_FILE = "indexation/reversed_index.txt"
DOCS_LINKS_FILE = "index.txt"

with open(DOCS_LINKS_FILE, "r") as file:
    doc_links = file.read().split()

parser = argparse.ArgumentParser(description='Reversed index search')
parser.add_argument('query', type=str, help='Search query')
args = parser.parse_args()

morph = MorphAnalyzer()

keywords = args.query.strip().split()
normalized_keywords = [morph.parse(keyword)[0].normal_form
                       for keyword in keywords]

index = {}

with open(INDEX_FILE) as file:
    for line in file.readlines():
        token, presences = line.split("\t")
        index[token] = [x == "1" for x in presences.split(" ")]

keywords_presences = []

for keyword in normalized_keywords:
    if keyword not in index:
        sys.exit("No results")

    keywords_presences.append(index[keyword])

bitwised_presences = keywords_presences[0]

if len(keywords_presences) > 1:
    bitwised_presences = np.bitwise_and.reduce(keywords_presences)

for doc_index, bitwised_value in enumerate(bitwised_presences):
    print(doc_links[doc_index + 1]) if bitwised_value else next
