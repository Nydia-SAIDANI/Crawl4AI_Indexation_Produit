import asyncio
from services.extractor import extract_products_llm, ensure_products_are_dicts
from services.indexer import index_products
from services.rag import generate_llm_answer
import os

if __name__ == "__main__":
    urls = [
        "https://www.zara.com/ca/en/sequin-mini-skirt-p03920221.html?v1=463145153",
        "https://www.walmart.ca/fr/ip/t-shirt-encolure-ras-du-cou-george-pour-femmes-gris/6000208213139?classType=VARIANT&athbdg=L1600",
        "https://www2.hm.com/en_ca/productpage.1292768002.html",
    ]
    products = asyncio.run(extract_products_llm(urls))
    products = ensure_products_are_dicts(products)
    collection = index_products(products)

    query = "Donnez moi les informations du pantalon ?"
    results = collection.query(query_texts=[query], n_results=3)
    metadatas = results["metadatas"][0]
    context = "\n".join(
        f"Produit : {m.get('titre', 'non trouvé')}\nPrix : {m.get('prix', 'non trouvé')}\nDescription : {m.get('description', 'non trouvé')}\nImage : {m.get('image_url', 'non trouvé')}\n"
        for m in metadatas
    )
    answer = generate_llm_answer(query, context, os.getenv("OPENAI_API_KEY"))
    print("Réponse RAG :", answer)



"""from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List

app = FastAPI()

class AnalyseRequest(BaseModel):
    urls: List[str]
    question: str

@app.post("/analyse")
async def analyse(request: AnalyseRequest):
    # Réponse en dur juste pour le test
    return {"answer": "Le produit le moins cher est le T-shirt bio coton à 14,99 €."}"""
