# services/vector_db.py
import os
import chromadb
from chromadb.utils import embedding_functions

# 📌 Base locale
client = chromadb.PersistentClient(path="./chroma_db")

# 📌 Embedding avec OpenAI
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"  # rapide et pas cher
)

# 📌 Collection pour les produits
collection = client.get_or_create_collection(
    name="produits",
    embedding_function=openai_ef
)

def add_products(products: list[dict]):
    """
    Stocke une liste de produits dans Chroma
    """
    for i, product in enumerate(products):
        # Texte combiné pour l'indexation
        text_for_embedding = f"{product.get('titre', '')} {product.get('description', '')} {product.get('prix', '')}"

        collection.add(
            ids=[f"product_{i}_{product.get('titre', '')}"],
            documents=[text_for_embedding],
            metadatas=[product]
        )

def search_products(query: str, n_results: int = 5):
    """
    Recherche les produits similaires à une requête
    """
    return collection.query(
        query_texts=[query],
        n_results=n_results
    )





"""from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import os

CHROMA_DIR = "chroma_store"

embedding = OpenAIEmbeddings()  

def index_products(products: list[dict]):
    texts = []
    metadatas = []

    for product in products:
        text = f"Titre: {product['title']}\nDescription: {product['description']}\nPrix: {product['price']}"
        texts.append(text)
        metadatas.append(product)

    db = Chroma.from_texts(texts, embedding=embedding, metadatas=metadatas, persist_directory=CHROMA_DIR)
    db.persist()"""