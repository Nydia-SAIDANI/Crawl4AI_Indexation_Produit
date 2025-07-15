import streamlit as st

st.title("Mini Site de Test")
st.write("Entrez jusqu'à 3 URLs de produits à analyser")

url1 = st.text_input("URL 1")
url2 = st.text_input("URL 2 (optionnel)")
url3 = st.text_input("URL 3 (optionnel)")

st.subheader("Posez vos questions")
question = st.text_input("Posez une question sur les produits à analyser :")

if st.button("Poser la question"):
    # on va appeler ton backend ici
    with st.spinner("Analyse en cours..."):
        st.success("Requête envoyée ! (à remplacer par vraie logique)")

    # (à remplacer par l’appel réel à l’API plus tard)
    st.subheader("Réponse IA :")
    st.write("Le produit le moins cher est le T-shirt bio coton à 14,99 €.")
