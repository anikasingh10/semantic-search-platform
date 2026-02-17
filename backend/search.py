import os


def load_documents():
    """
    Load documents from the dataset file
    """
    file_path = os.path.join("backend", "documents", "data.txt")

    with open(file_path, "r") as f:
        lines = f.readlines()

    # clean and remove empty lines
    documents = [line.strip() for line in lines if line.strip()]

    return documents