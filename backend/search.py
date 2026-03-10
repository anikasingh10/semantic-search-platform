import os
import re
import numpy as np
import faiss

from embedder import create_embedding
from pdf_loader import clean_text


def load_documents():
    """Load documents from the dataset file."""
    file_path = os.path.join("documents", "data.txt")

    with open(file_path, "r") as f:
        lines = f.readlines()

    # clean and remove empty lines
    documents = [clean_text(line) for line in lines if line.strip()]

    return documents


documents = load_documents()

document_chunks = []

embeddings = []

for doc in documents:
    document_chunks.append(doc)
    embeddings.append(create_embedding(doc))

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


def chunk_text(text: str, max_words: int = 250):
    """Split text into readable chunks based on sentence boundaries."""

    text = clean_text(text)

    # Split by sentence boundaries (keep punctuation attached to the sentence).
    sentences = re.split(r"(?<=[\.\?!])\s+", text)

    chunks = []
    current_chunk: list[str] = []
    current_word_count = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        words = sentence.split()
        if not words:
            continue

        # If a single sentence is very long, split it by word count.
        if len(words) >= max_words:
            if current_chunk:
                chunks.append(" ".join(current_chunk).strip())
                current_chunk = []
                current_word_count = 0

            for i in range(0, len(words), max_words):
                chunks.append(" ".join(words[i : i + max_words]).strip())
            continue

        if current_word_count + len(words) > max_words and current_chunk:
            chunks.append(" ".join(current_chunk).strip())
            current_chunk = []
            current_word_count = 0

        current_chunk.append(sentence)
        current_word_count += len(words)

    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks


def index_document(text):
    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = create_embedding(chunk)

        vector = np.array([embedding]).astype("float32")

        index.add(vector)

        document_chunks.append(chunk)