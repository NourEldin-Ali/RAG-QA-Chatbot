from langchain.document_loaders import TextLoader
import os

def read_docs(docs_path:str):
    """
    Read the documentation from the txt files.
    """
    if(docs_path is None):
        raise ValueError("Documents path is not defined")
    
    documents = []
    for file in os.listdir(docs_path):
        if file.endswith(".txt"):  # Adjust for other formats if needed
            loader = TextLoader(os.path.join(docs_path, file))
            documents.extend(loader.load())
    return documents