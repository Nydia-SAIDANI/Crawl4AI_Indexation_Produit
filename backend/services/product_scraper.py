import asyncio
import json
from playwright.async_api import async_playwright
from services.extractor import extract_product_details_with_llm


async def scrape_products_from_category(category_url: str, browser, max_products: int = 10):
    """
    Scrape une seule catégorie produit (1 URL).
    Le navigateur Playwright est passé en paramètre pour être réutilisé.
    """
    results = []
    page = await browser.new_page()
    await page.goto(category_url, timeout=60000)

    print(f"Scraping de {category_url}")
    print("Attente du conteneur principal...")
    await page.wait_for_selector("ul.product-grid__product-list")

    print("Scroll pour charger les produits...")
    for _ in range(15):
        await page.mouse.wheel(0, 1000)
        await asyncio.sleep(2)

    print("Recherche des blocs produits...")
    products = await page.query_selector_all("ul.product-grid__product-list > li.products-category-grid-block")
    print(f"Nombre de produits détectés : {len(products)}")

    product_urls = []
    for product in products:
        link_el = await product.query_selector("a.product-link")
        link = await link_el.get_attribute("href") if link_el else None
        if link:
            full_link = f"https://www.zara.com{link}" if link.startswith("/") else link
            product_urls.append(full_link)

    print(f"{len(product_urls)} liens de produits collectés. Extraction via Crawl4AI en cours...")

    for i, url in enumerate(product_urls[:max_products]):
        print(f"\n Produit {i+1} - {url}")

        # Pour Ouvrrir UNE NOUVELLE PAGE Playwright pour CHAQUE produit
        product_page = await browser.new_page()
        await product_page.goto(url, timeout=60000)

        # Image principale
        await product_page.wait_for_selector("img.media-image__image[src*='.jpg']", timeout=10000)
        imgs = await product_page.query_selector_all("img.media-image__image")
        product_img_src = None
        for img in imgs:
            src = await img.get_attribute("src")
            if src and ".jpg" in src:
                product_img_src = src
                break

        # Extraction avec LLM
        data = await extract_product_details_with_llm(url)
        if data:
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except Exception as e:
                    print(f"❌ Erreur de parsing JSON : {e}")
                    continue
            if isinstance(data, dict):
                data["image"] = product_img_src or data.get("image")
                results.append(data)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        item["image"] = product_img_src or item.get("image")
                results.extend(data)
            else:
                print("❌ Format de données inattendu :", type(data))
        else:
            print("❌ Aucune donnée extraite.")

        await product_page.close()

    await page.close()
    return results


async def scrape_multiple_categories(urls: list[str], max_products: int = 10):
    """
    Scrape plusieurs catégories produit (1 à N URLs).
    Réutilise le même navigateur Playwright.
    """
    all_results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        for url in urls:
            try:
                products = await scrape_products_from_category(url, browser, max_products=max_products)
                all_results.extend(products)
            except Exception as e:
                print(f"❌ Erreur lors du scraping de {url} : {e}")
        await browser.close()
    return all_results