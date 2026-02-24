import os
import numpy as np
import faiss

from embedder import create_embedding


def load_documents():
    """
    Load documents from the dataset file
    """
    file_path = os.path.join("documents", "data.txt")

    with open(file_path, "r") as f:
        lines = f.readlines()

    # clean and remove empty lines
    documents = [line.strip() for line in lines if line.strip()]

    return documents

documents = load_documents()

# convert documents into embeddings
embeddings = [create_embedding(doc) for doc in documents]

# convert to numpy array
embedding_matrix = np.array(embeddings).astype("float32")

# get vector dimension
dimension = embedding_matrix.shape[1]

# create FAISS index
index = faiss.IndexFlatL2(dimension)

# add embeddings to index
index.add(embedding_matrix)


def search(query, k=3):
    """
    Perform semantic similarity search
    """

    query_embedding = create_embedding(query)
    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, k)

    results = [document_chunks[i] for i in indices[0]]

    return results

def chunk_text(text, chunk_size=200):
    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

document_chunks = []

def index_document(text):
    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = create_embedding(chunk)

        vector = np.array([embedding]).astype("float32")

        index.add(vector)

        document_chunks.append(chunk)