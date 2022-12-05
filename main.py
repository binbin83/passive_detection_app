"""Script for the application, 


"""

import streamlit as st
import pandas as pd
import numpy as np

import re

from src.PassivePySrcFR.PassivePy import PassivePyAnalyzer
from src.analysis_passive import load_from_text


def load_analyzer():
    analyzer= PassivePyAnalyzer(spacy_model= "fr_core_news_lg")
    return analyzer

if __name__ =="__main__":
    st.set_page_config(
        page_title="Détection de la voix passive dans un texte Français", page_icon="📘"
    )

    st.title("Détection de la voix passive dans un texte en  Français")

    analyzer = load_analyzer()



    with st.form(key='text_entry'):

        text = st.text_input(label='Entrer une phrase:', max_chars=500)
        print(text)
        submit_button = st.form_submit_button(label='🏷️ Go !')

    if submit_button:
        if re.sub('\s+','',text)=='':
            st.error('Entrer une phrase plus longue ! ')

        elif re.match(r'\A\s*\w+\s*\Z', text):
            st.error("Entrer une phrase plus longue !")
    
        else:
            st.markdown("### Résultats : ")
            st.header("")
            results = load_from_text(text,analyzer=analyzer)
            st.table(results)
            
            st.markdown("### Concernant le parsing du texte : ")
            st.header("")
            parsing = analyzer.parse_sentence(text)
            st.table(parsing)




    st.header("")
   
    with st.expander("ℹ️ - A propos de cette application", expanded=True):


        st.write(
            """     
            - Cette page a été créée dans le cadre d'une collaboration entre chercheurs issues de différentes disciplines.
            - Elle a pour but de détecter la voix passive dans un texte en Français.
            - Elle repose principalement sur le modèle "fr_core_news_lg" de la bibliothèque Spacy
            - Elle est inspirée de ce répertoire github: https://github.com/mitramir55/PassivePy 
            """
            )