import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def answer_question_with_rag(question: str, context: str) -> str:
    """
    Génère une réponse à partir d'une question et d'un contexte
    """
    prompt = f"""
    Contexte : {context}

    Question : {question}

    Réponds de manière claire en utilisant uniquement les informations du contexte.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 
        messages=[
            {"role": "system", "content": "Tu es un assistant expert en analyse de produits e-commerce."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content



"""from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI  
from vector_store import CHROMA_DIR, embedding 

def answer_question_with_rag(collection, question):
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n".join(results["documents"][0])
    prompt = f"Voici des produits Zara:\n{context}\n\nQuestion: {question}\nRéponse :"

    # Envoi à OpenAI ou un autre modèle
    import openai
    openai.api_key = "OPENAI_API_KEY"
    response = openai.ChatCompletion.create(
        model="openai/gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
"""