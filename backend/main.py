import chromadb
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.product_scraper import scrape_multiple_categories, scrape_products_from_category
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
    urls: list[str]
    question: str

@app.post("/analyze")
async def analyze_url(request: AnalyzeRequest):
    try:
        # Scraper toutes les URLs
        products = await scrape_multiple_categories(request.urls)

        if not isinstance(products, list) or not all(isinstance(p, dict) for p in products):
            return {"error": "Les données ne sont pas valides."}


        add_products(products)


        docs = search_products(request.question, n_results=5)
        """context = "\n\n".join(docs["documents"][0])"""
        context = "\n\n".join(
    [doc for docs_list in docs["documents"] for doc in docs_list]
)
        rag_answer = answer_question_with_rag(request.question, context)


        print("PRODUCTS:", products)


        return {
            "products": products,
            "answer": rag_answer
        }

    except Exception as e:
        print(f"[ERREUR] {str(e)}")
        return {"error": str(e)}



