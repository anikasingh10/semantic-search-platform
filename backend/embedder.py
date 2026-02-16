from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):
    """
    Convert input text into an embedding vector
    """
    embedding = model.encode(text)
    return embedding