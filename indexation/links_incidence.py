import numpy as np
import os

ROOT_URL = "https://nekdo.ru"
LINKS_PATH = "docs/links/"
INDEX_PATH = "indexation/"
INDEX_FILE_NAME = "links_incidence_index.txt"
LINKS_INDEX_PATH = "index.txt"

docs_list = os.listdir(LINKS_PATH)

index = np.zeros((100, 100))

with open(LINKS_INDEX_PATH, "r") as file:
    paths = [link.strip()[len(ROOT_URL):] for link in file.readlines()]

for filename in docs_list:
    with open(LINKS_PATH + filename, "r") as file:
        doc_index = int(filename.split(".")[0]) - 1
        links = file.read().strip().split(" ")
        for link in set(links):
            if link not in paths:
                continue

            index[doc_index][paths.index(link)] = 1


with open(INDEX_PATH + INDEX_FILE_NAME, "w") as result_file:
    for links_presences in index:
        index_row = " ".join([str(int(pres)) for pres in links_presences])
        result_file.write(index_row + "\n")
