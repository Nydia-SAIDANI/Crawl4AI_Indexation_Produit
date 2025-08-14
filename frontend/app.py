import streamlit as st
import requests

st.title("🛍️ Analyse de produits E-commerce")

url = st.text_input("Entrez l'URL de la catégorie produit", placeholder="https://www.zara.com/...")
st.subheader("Posez vos questions")
question = st.text_input("Posez une question sur les produits à analyser :")

if st.button("Analyser et répondre"):
    if url and question:
        with st.spinner("🔄 Traitement en cours..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"url": url, "question": question}
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Extraction réussie !")
                    # st.dataframe(result["products"])
                    st.markdown(f"**💬 Réponse :** {result['answer']}")
                else:
                    st.error(f"❌ Erreur serveur : {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Erreur de connexion au backend : {e}")
    else:
        st.warning("⚠️ Veuillez entrer une URL et une question.")
