import os
import json
from crawl4ai import LLMConfig, LLMExtractionStrategy, CrawlerRunConfig, AsyncWebCrawler
from models.product import ProductInfo

async def extract_product_details_with_llm(url: str):
    api_key = os.getenv("OPENAI_API_KEY")

    instruction = """Tu es un expert en extraction produit. À partir du contenu de la page, génère ce JSON : 
    {"titre": "...", "description": "...", "prix": "...", "image": "..."}. Indique "non trouvé" si un champ manque."""

    llm_config = LLMConfig(
        provider="openai/gpt-3.5-turbo",
        api_token=api_key,
        temperature=0
    )

    strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        schema=ProductInfo.model_json_schema(),
        extraction_type="schema",
        instruction=instruction
    )

    run_config = CrawlerRunConfig(extraction_strategy=strategy)

    async with AsyncWebCrawler() as crawler:
        try:
            result = await crawler.arun(url=url, config=run_config)
            return result.extracted_content if result.extracted_content else None
        except Exception as e:
            print(f"❌ Erreur pour {url} : {e}")
            return None
