import streamlit as st
from utils import *

st.set_page_config(page_title="Assistant Jardinage", page_icon="🌿")
st.title("🌻 Assistant IA - Jardinage")

st.markdown("Cette application utilise **tous les documents PDF** stockés sur Azure Blob pour répondre à vos questions.")

question = st.text_input("Quelle est votre question ?")

if st.button("Poser la question") and question:
    with st.spinner("Je lis tous les documents Azure..."):
        try:
            texte_pdf = lire_tous_les_pdfs_du_dossier()
        except Exception as e:
            st.error(f"Erreur : {e}")
            texte_pdf = ""

        if texte_pdf:
            contexte = texte_pdf[:4000]
            reponse = poser_question(question, contexte)
            st.success(reponse)
        else:
            st.error("Aucun contenu extrait des documents.")
