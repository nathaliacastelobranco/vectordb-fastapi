from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
    )
from langchain_chroma import Chroma
import warnings
import shutil
import os

warnings.filterwarnings('ignore')

# Creating database
def create_db():
    # Load document
    loader = PyPDFLoader("files\[CILAMCE 2021] Artigo_Nathalia.pdf")
    pages = loader.load()

    # Splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100,length_function=len,
            is_separator_regex=False)
    chunks = text_splitter.split_documents(pages)

    # Embeddings
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Persists embeddings to vector database
    ids = [str(i) for i in range(1, len(chunks) + 1)]
    Chroma.from_documents(pages, embedding_function, persist_directory="chroma_db", ids=ids)

#Deleting the database
def delete_persisted_db():
    if "chroma_db" in os.listdir():
        shutil.rmtree("chroma_db")
        print(f"Deleted database and its contents.")
    else:
        raise FileNotFoundError("Database not found.")