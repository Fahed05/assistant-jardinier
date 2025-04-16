import streamlit as st
import os
from app.utils import lire_pdf, poser_question

st.set_page_config(page_title="Assistant Jardinage", page_icon="🌿")
st.title("🌻 Assistant IA - Jardinage")
st.markdown("Téléverse un guide PDF et pose une question dessus.")

uploaded_file = st.file_uploader("Choisir un fichier PDF", type=["pdf"])

if uploaded_file:
    file_path = os.path.join("data", uploaded_file.name)
    os.makedirs("data", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    texte_pdf = lire_pdf(file_path)
    question = st.text_input("Quelle est ta question ?")

    if st.button("Poser la question") and question:
        with st.spinner("Je réfléchis... 🧠"):
            reponse = poser_question(question, texte_pdf[:4000])
            st.markdown("### Réponse :")
            st.success(reponse)
