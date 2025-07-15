import requests
import streamlit as st

st.title("Mini Site de Test")
st.write("Entrez jusqu'à 3 URLs de produits à analyser")

url1 = st.text_input("URL 1")
url2 = st.text_input("URL 2 (optionnel)")
url3 = st.text_input("URL 3 (optionnel)")

st.subheader("Posez vos questions")
question = st.text_input("Posez une question sur les produits à analyser :")

if st.button("Poser la question"):
    with st.spinner("Analyse en cours..."):
        urls = [url for url in [url1, url2, url3] if url]
        payload = {"urls": urls, "question": question}
        try:
            response = requests.post("http://localhost:8000/analyse", json=payload)
            result = response.json()
            st.subheader("Réponse IA :")
            st.write(result.get("answer", "Aucune réponse"))
        except Exception as e:
            st.error(f"Erreur : {e}")
