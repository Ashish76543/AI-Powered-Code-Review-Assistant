import faiss##used to store and search vectors efficiently 
import numpy as np
import os
import json

DIMENSION = 384##vector size for entry into faiss

INDEX_PATH = "app/vectorstore/index.faiss"##location where the vector database is stored
METADATA_PATH = (
    "app/vectorstore/metadata.json"
)

if os.path.exists(INDEX_PATH):

    index = faiss.read_index(
        INDEX_PATH
    )

else:

    index = faiss.IndexFlatL2(##store vector flat and uses L2 ,euclidena distance for comparison
        DIMENSION
    )
##if the vector db already exists load it if not create a new one 

def save_index():

    faiss.write_index(
        index,
        INDEX_PATH
    ) ## save index to disk in the path


def add_embedding(vector):

    vector = np.array(
        [vector]
    ).astype("float32")

    index.add(vector)

    save_index()

## to add embedding  




def save_metadata(data):

    with open(
        METADATA_PATH,
        "w"
    ) as f:

        json.dump(
            data,
            f
        )


def load_metadata():

    with open(
        METADATA_PATH,
        "r"
    ) as f:

        return json.load(f)
    

##used to map the metadat ie file name to the vector number and save metadat and vector
def add_code_embedding(
    vector,
    filename
):

    metadata = load_metadata()

    vector_id = len(metadata)

    add_embedding(vector)

    metadata[str(vector_id)] = {
        "filename": filename
    }

    save_metadata(metadata)

def search_similar(
    vector,
    k=3
):
##3 for return top 3 similar result
    vector = np.array(
        [vector]
    ).astype("float32")
##convert the vector to np array

    distances, indices = (
        index.search(
            vector,
            k
        )
    )
    ##search for the vector we get index and distance

    metadata = load_metadata()
##get all meta data
    results = []

    for idx in indices[0]:
##go through each vector in indices 
        if str(idx) in metadata:
##check if the vectoris present as keys if soappend ti resuls the file nameand return it
            results.append(
                metadata[
                    str(idx)
                ]
            )

    return results