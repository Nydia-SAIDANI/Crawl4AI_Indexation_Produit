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
        if not urls or not question:
            st.error("Veuillez entrer au moins une URL et une question.")
        else:
            try:
                # Étape 1 : Appeler /extract pour récupérer et indexer les produits
                extract_response = requests.post("http://localhost:8000/extract", json={"urls": urls})
                extract_response.raise_for_status()

                # Étape 2 : Appeler /ask pour poser la question
                ask_response = requests.post("http://localhost:8000/ask", json={"question": question})
                ask_response.raise_for_status()
                result = ask_response.json()

                st.subheader("Réponse IA :")
                st.write(result.get("answer", "Aucune réponse"))
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de requête : {e}")
            except Exception as e:
                st.error(f"Erreur inattendue : {e}")
