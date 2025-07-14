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