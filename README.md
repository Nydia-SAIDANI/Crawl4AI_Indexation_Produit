    Crawl4ai et Mini Site pour Indexer des Produits

Créer l'env virtuel:
C:\Users\Admin\Documents\crawl4ai_mini_project>"C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe" -m venv venv

Activer l'env :
C:\Users\Admin\Documents\crawl4ai_mini_project>venv\Scripts\activate

MAJ:
python -m pip install --upgrade pip setuptools wheel

Installation FastApi:
python -m pip install fastapi uvicorn

(venv) C:\Users\Admin\Documents\crawl4ai_mini_project>pip freeze > backend/requirements.txt

(venv) C:\Users\Admin\Documents\crawl4ai_mini_project>pip install python-dotenv

Tester le fonctionnement de FastApi:
uvicorn backend.main:app --reload

Validation du fonctionnement:
Exécution sur : 
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

Web cwawling and scraping 

Install Crawl4AI and its dependencies
pip install -U crawl4ai

Installs browser dependencies for dynamic crawling
python -m playwright install --with-deps chromium

Installation validation:
crawl4ai-doctor -didn't work
"C:/Users/Admin/AppData/Roaming/Python/Python313/Scripts/crawl4ai-doctor.exe"

Lancer l'app avec FastApi
uvicorn main:app --host 127.0.0.1 --port 8000

openai API Key
https://platform.openai.com/api-keys