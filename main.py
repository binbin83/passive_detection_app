"""Script for the application, 


"""
import pandas as pd
import numpy as np
import streamlit as st
from spacy_streamlit import visualize_spans



import re

from src.PassivePySrcFR.PassivePy import PassivePyAnalyzer
from src.analysis_passive import load_from_text


color_dict = {
    "passif_tronqué": "#8ef",
    "passive_rule_2" : "#faa",
    "passif_sequencé" : "afa",
    "passif_impersonel":"#fea",
    "passive_rule_5":"#faa",
    "passif_verbale":"#000080",
    "passif_factif" : "#00FF00",
    "passif_adjectif":"#808080",
    "passif_canonique":"#29e61a"  
}


def load_analyzer():
    analyzer= PassivePyAnalyzer(spacy_model= "fr_core_news_lg")
    return analyzer

if __name__ =="__main__":
    st.set_page_config(
        page_title="Détection de la voix passive dans un texte Français", page_icon="📘"
    )

    
    st.title("Détection de la voix passive dans un texte en  Français")

    st.markdown("### Quelques prérequis: ")
    st.markdown("La voix passive en Français peut prendre différentes formes :")
    st.markdown("- La voix passive canonique: être + Particpe Passé + par; **exemple**: J'ai été frappé par un homme.")
    st.markdown("- La voix passive tronqué: être + Particpe Passé; **exemple**: J'ai été frappé. ")
    st.markdown("- La voix passive en sequence: être + Particpe Passé + conjonction de coordination + PP; **exemple**: J'ai été frappé et emmené. ")
    st.markdown("- La voix passive verbal: verbe auant un sens passif par nature; **exemple**: J'ai subi un interrogatoire. ")
    st.markdown("- La voix passive factice : faire + Particpe Passé; **exemple**: On s'est fait frappé. ")
    st.markdown("- Les adjectif passifs : -ible/-able; **exemple**: visible (il y a des exceptions). ")

    analyzer = load_analyzer()

    st.header("")
    st.markdown("### Détection automatique:")
    


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
            st.markdown("### La voix passive dans le texte: ")
            st.header("")
            matches, doc = analyzer.prepare_visualisation(text)
            if matches :
                visualize_spans(doc, spans_key="passive",displacy_options={"colors": color_dict}, show_table =  False, title = "")
            else :
                st.markdown("Nous n'avons pas identifier de voix passive dans votre texte")
            st.markdown("### les réultats en chiffres: ")
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
            - Plus d'information sur la voix passive en Français : https://hal.archives-ouvertes.fr/halshs-01465258/ 
            - Elle est inspirée de ce répertoire github: https://github.com/mitramir55/PassivePy 
            - Développé par  Robin Quillivic dans le cadre de son doctorat à l'EPHE
            """
            )
    
