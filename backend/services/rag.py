import openai

def generate_llm_answer(question, context, api_key):
    client = openai.OpenAI(api_key=api_key)
    prompt = f"""Tu es un assistant expert des produits. Voici les informations extraites :
{context}

Réponds à la question suivante en te basant uniquement sur ce contexte : "{question}"
Si la réponse n’est pas clairement présente, réponds "Information non trouvée".
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
