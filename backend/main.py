import chromadb
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import asyncio

from services.product_scraper import scrape_products_from_category
from services.vector_store import add_products, search_products

from services.rag import answer_question_with_rag
app = FastAPI()

# Pour permettre les requêtes entre Streamlit (frontend) et FastAPI (backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class AnalyzeRequest(BaseModel):
    url: str
    question: str

@app.post("/analyze")
async def analyze_url(request: AnalyzeRequest):
    try:
        # 1️⃣ Scraper
        products = await scrape_products_from_category(request.url)

        if not isinstance(products, list) or not all(isinstance(p, dict) for p in products):
            return {"error": "Les données ne sont pas valides."}

        # 2️⃣ Stocker dans Chroma
        add_products(products)

        # 3️⃣ RAG : recherche + réponse
        docs = search_products(request.question, n_results=5)

        # On combine les documents pour le contexte
        context = "\n\n".join([doc for doc in docs["documents"][0]])
        rag_answer = answer_question_with_rag(request.question, context)

        return {
            "products": products,
            "answer": rag_answer
        }

    except Exception as e:
        print(f"[ERREUR] {str(e)}")
        return {"error": str(e)}




    """@app.get("/search")
async def search(query: str):
    results = search_products(query)
    return results
try:
        products = await scrape_products_from_category(request.url)

        print(f"[DEBUG] Type : {type(products)}")
        print(f"[DEBUG] Exemple produit : {products[0] if products else 'vide'}")

        if not isinstance(products, list) or not all(isinstance(p, dict) for p in products):
            return {"error": "Les données ne sont pas valides."}

        return {"products": products}

    except Exception as e:
        print(f"[ERREUR] {str(e)}")
        return {"error": str(e)}"""


"""@app.post("/analyze")
async def analyze_url(request: AnalyzeRequest):
    print(f"Requête reçue avec URL : {request.url}")
    try:
        products = await scrape_products_from_category(request.url)
        
        # Vérification du type
        print(f"Type de 'products' : {type(products)}")
        
        # Affichage d'un exemple
        if products:
            print(f"Premier produit : {products[0]}")
            print(f"Type du premier produit : {type(products[0])}")

        # Validation explicite
        if not isinstance(products, list) or not all(isinstance(p, dict) for p in products):
            return {"error": "Les données retournées ne sont pas une liste de dictionnaires"}
        
        return {"products": products}

    except Exception as e:
        return {"error": str(e)}"""