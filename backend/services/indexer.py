import os
import chromadb
from chromadb.utils import embedding_functions

def index_products(products: list):
    try:
        embedding_func = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )

        chroma_client = chromadb.Client()

        try:
            collection = chroma_client.get_collection("produits", embedding_function=embedding_func)
            existing_ids = collection.get()["ids"]
            if existing_ids:
                collection.delete(ids=existing_ids)
        except Exception:
            # créetr la collection
            collection = chroma_client.create_collection("produits", embedding_function=embedding_func)

        for idx, prod in enumerate(products):
            if isinstance(prod, dict) and prod.get("titre", "non trouvé") != "non trouvé":
                doc = f"""{prod.get("titre", "")}
{prod.get("description", "")}
{prod.get("prix", "")}"""
                collection.add(documents=[doc], metadatas=[prod], ids=[str(idx)])

        return collection

    except Exception as e:
        
        raise RuntimeError(f"Échec de l'indexation : {e}")