from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sys
import asyncio
import os
from services.extractor import extract_products_llm, ensure_products_are_dicts
from services.indexer import index_products
from services.rag import generate_llm_answer
import traceback

app = FastAPI()

# Stockage temporaire en mémoire
memory_store = {
    "collection": None,
    "products": [],
}

class URLRequest(BaseModel):
    urls: List[str]

class QuestionRequest(BaseModel):
    question: str

@app.post("/extract")
async def extract_products(request: URLRequest):
    try:
        products = await extract_products_llm(request.urls)
        products = ensure_products_are_dicts(products)
        collection = index_products(products)
        memory_store["collection"] = collection
        memory_store["products"] = products
        return {"products": products}
    except Exception as e:
        # Afficher les détails de l'erreur dans le terminal
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction des produits: {str(e)}")
    

@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        collection = memory_store.get("collection")
        if not collection:
            raise HTTPException(status_code=400, detail="Aucune donnée indexée.")

        results = collection.query(query_texts=[request.question], n_results=3)
        metadatas = results["metadatas"][0]
        context = "\n".join(
            f"Produit : {m.get('titre', 'non trouvé')}\nPrix : {m.get('prix', 'non trouvé')}\nDescription : {m.get('description', 'non trouvé')}\nImage : {m.get('image_url', 'non trouvé')}\n"
            for m in metadatas
        )
        answer = generate_llm_answer(request.question, context, os.getenv("OPENAI_API_KEY"))
        return {"answer": answer}

    except HTTPException:
       
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la réponse: {str(e)}")

"""import sys
import asyncio
from playwright.async_api import async_playwright

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

import os

from services.extractor import extract_products_llm, ensure_products_are_dicts
from services.indexer import index_products
from services.rag import generate_llm_answer



app = FastAPI()

# Stockage temporaire en mémoire
memory_store = {
    "collection": None,
    "products": [],
}

class URLRequest(BaseModel):
    urls: List[str]

class QuestionRequest(BaseModel):
    question: str

@app.post("/extract")
async def extract_products(request: URLRequest):
    try:
        products = await extract_products_llm(request.urls)
        products = ensure_products_are_dicts(products)
        collection = index_products(products)
        memory_store["collection"] = collection
        memory_store["products"] = products
        return {"products": products}
    except Exception as e:
        import traceback
        traceback.print_exc()  # ← Affiche l’erreur complète dans le terminal
        raise HTTPException(status_code=500, detail=str(e))  # ← Affiche le message dans Swagger


@app.post("/ask")
def ask_question(request: QuestionRequest):
    collection = memory_store.get("collection")
    if not collection:
        raise HTTPException(status_code=400, detail="Aucune donnée indexée. Appelez /extract d'abord.")
    
    results = collection.query(query_texts=[request.question], n_results=3)
    metadatas = results["metadatas"][0]
    context = "\n".join(
        f"Produit : {m.get('titre', 'non trouvé')}\nPrix : {m.get('prix', 'non trouvé')}\nDescription : {m.get('description', 'non trouvé')}\nImage : {m.get('image_url', 'non trouvé')}\n"
        for m in metadatas
    )
    answer = generate_llm_answer(request.question, context, os.getenv("OPENAI_API_KEY"))
    return {"answer": answer}"""




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
