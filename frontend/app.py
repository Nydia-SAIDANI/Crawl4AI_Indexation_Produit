import streamlit as st
import requests

st.title("🛍️ Analyse de produits E-commerce")


url1 = st.text_input("Entrez l'URL 1 :")
url2 = st.text_input("Entrez l'URL 2 (optionnel) :")
url3 = st.text_input("Entrez l'URL 3 (optionnel) :")

question = st.text_input("Posez une question sur les produits :")

if st.button("Analyser et poser la question"):
    urls = [u for u in [url1, url2, url3] if u] 

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
                
                # Stocker résultats dans session_state
                st.session_state["products"] = data.get("products", [])
                st.session_state["answer"] = data.get("answer", "Aucune réponse disponible.")
            else:
                st.error(f"❌ Erreur serveur : {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")

# Afficher la réponse et produits seulement si analyse déjà faite
if "answer" in st.session_state:
    st.subheader("Réponse à votre question")
    st.write(st.session_state["answer"])

if "products" in st.session_state:
    products = st.session_state["products"]

    if products:
        st.subheader("Produits récupérés")

        # Filtrer par mot-clé dans le titre
        keyword_filter = st.text_input("Filtrer par mot-clé dans le titre :")

        filtered_products = products
        if keyword_filter:
            filtered_products = [
                p for p in products 
                if keyword_filter.lower() in p.get("titre", "").lower()
            ]

        # Trier par prix
        sort_option = st.selectbox("Trier par prix :", ["Aucun", "Croissant", "Décroissant"])

        def parse_price(p):
            try:
                return float(p.get("prix", "0").replace("€", "").replace("$", "").replace(",", "."))
            except:
                return 0.0

        if sort_option == "Croissant":
            filtered_products.sort(key=parse_price)
        elif sort_option == "Décroissant":
            filtered_products.sort(key=parse_price, reverse=True)

        #  Affichage en grille 
        if filtered_products:
            cols = st.columns(3)
            
            for i, p in enumerate(filtered_products):
                with cols[i % 3]:
                    if p.get("image"):
                        st.image(p.get("image"), width=150)
                    st.markdown(f"**{p.get('titre', 'Titre non trouvé')}**")
                    st.markdown(f"Prix : {p.get('prix', 'Non trouvé')}")
                    st.markdown(f"{p.get('description', 'Description non trouvée')}")
                    st.markdown("---")
        else:
            st.info("Aucun produit correspondant à vos critères.")
