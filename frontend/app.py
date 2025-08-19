import streamlit as st
import requests

st.title("🛍️ Analyse de produits E-commerce")

# Champs pour 3 URLs max
url1 = st.text_input("Entrez l'URL 1 :")
url2 = st.text_input("Entrez l'URL 2 (optionnel) :")
url3 = st.text_input("Entrez l'URL 3 (optionnel) :")

question = st.text_input("Posez une question sur les produits :")

if st.button("Analyser et poser la question"):
    urls = [u for u in [url1, url2, url3] if u]  # filtrer les vides

    if not urls:
        st.warning("Veuillez entrer au moins une URL.")
    elif not question.strip():
        st.warning("Veuillez poser une question.")
    else:
        payload = {
            "urls": urls,
            "question": question
        }
        try:
            response = requests.post("http://localhost:8000/analyze", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Analyse terminée")
                st.write("**Réponse RAG :**", data["answer"])

                with st.expander("Produits récupérés :"):
                    for p in data["products"]:
                        st.write(p)
            else:
                st.error(f"❌ Erreur serveur : {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")
