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
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "Tu es un assistant expert en analyse de produits e-commerce."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

