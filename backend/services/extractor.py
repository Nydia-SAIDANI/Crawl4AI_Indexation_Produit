import os
import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy
from crawl4ai.chunking_strategy import OverlappingWindowChunking
from models.product import ProductInfo

def merge_chunks(extracted_chunks: list) -> dict:
    merged = {}
    for chunk in extracted_chunks:
        for k, v in chunk.items():
            if not v or v == "non trouvé":
                continue
            if k not in merged or not merged[k] or merged[k] == "non trouvé":
                merged[k] = v
    for key in ["titre", "description", "prix", "image_url"]:
        if key not in merged:
            merged[key] = "non trouvé"
    return merged

async def extract_products_llm(urls: List[str]) -> List[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    instruction = """
Tu es un expert en extraction produit. À partir du contenu de la page, génère ce JSON : 
{"titre": "...", "description": "...", "prix": "...", "image_url": "..."}.
Indique "non trouvé" si un champ manque.
"""
    chunker = OverlappingWindowChunking(window_size=1000, overlap=50)
    results = []
    async with AsyncWebCrawler() as crawler:
        for url in urls:
            strategy = LLMExtractionStrategy(
                llm_config=LLMConfig(provider="openai/gpt-3.5-turbo", api_token=api_key),
                schema=ProductInfo.model_json_schema(),
                extraction_type="schema",
                instruction=instruction,
                chunking_strategy=chunker,
            )
            run_config = CrawlerRunConfig(extraction_strategy=strategy)
            try:
                result = await crawler.arun(url=url, config=run_config)
                extracted = result.extracted_content
                if isinstance(extracted, list):
                    merged = merge_chunks(extracted)
                    results.append(merged)
                else:
                    results.append(extracted)
            except Exception as e:
                results.append({"error": str(e)})
    return results

def ensure_products_are_dicts(products):
    import json
    proper_products = []
    for prod in products:
        if isinstance(prod, str):
            try:
                parsed = json.loads(prod)
                if isinstance(parsed, list):
                    proper_products.extend(parsed)
                elif isinstance(parsed, dict):
                    proper_products.append(parsed)
            except Exception:
                pass
        elif isinstance(prod, dict):
            proper_products.append(prod)
    return proper_products
