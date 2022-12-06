[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://passive-fr.streamlit.app/)

# Détection de la voix passive dans le Français parlé





- [0. A propos](#0-a-propos)
- [1. Prérequis sur le passif en français](#prérequis-sur-le-passif-en-français)
- [2. Fonctionnement de l'application](#2-fonctionnement-de-lapplication)
- [3. Instalation](#3-instalation)
- [4. Limitations](#4-limitations)
- [5. To do](#5-to-do)

## 0. A propos
Cette application permet de détecter la voix passive dans un texte en Français. 

Le code source s'inspire en grande partie de ce projet : <a href = "https://github.com/mitramir55/PassivePy"> PassivePy</a>

L'application public streamlit associée est disponible en ligne:   <a href = "https://passive-fr.streamlit.app/"> lien streamlit</a> 


Auteur: <a href="https://www.linkedin.com/in/robin-quillivic/">Robin Quillivic</a>, Doctorant  (1A)  EPHE - Institut des Systèmes Complexes

## 1. Prérequis sur le passif en français
La voix passive en Français peut prendre différentes formes :
- La voix passive canonique: être + Particpe Passé d'un verbe transitif+ par;**exemple**: J'ai été frappé par un homme.
- La voix passive tronqué: être + Particpe Passé d'un verbe transitif; **exemple**: J'ai été frappé.
- La voix passive en sequence: être + Particpe Passé + conjonction de coordination + PP; **exemple**: J'ai été frappé et emmené.
- La voix passive verbal: verbe auant un sens passif par nature; **exemple**: J'ai subi un interrogatoire. ")
- La voix passive factice : se + faire + Particpe Passé; **exemple**: On s'est fait frappé. 
- Les adjectifs passifs : -ible/-able; **exemple**: visible (il y a des exceptions).
- Plus d'information sur la voix passive en Français : https://hal.archives-ouvertes.fr/halshs-01465258/ 

## 2. Fonctionnement de l'application

Afin d'identifier la voix passive dans un texte, nous utilisons les régles de grammaires présenter plus haut. L'ensemble de ces règles sont encapsulées dans un Matcher() Spacy, voir fichier: *src/PassivePySrcFR/rules_for_all_passives*
Par exemple, la régle concernant le passif canonique est codé comme suit :
```
passive_rule_0 = [
        {"POS":"AUX", "DEP": "aux", "OP":"*"},
        {"POS":"AUX", "DEP": "aux:pass", "OP":"+"},
        {"DEP":"neg", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"DEP":"HYPH", "OP":"*"},
        {"DEP":"advmod", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"POS":"VERB", "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part"]}, "LEMMA":{"NOT_IN" : verbs_list }},
        {"LOWER":"par"}
    ]
```

## 3. Instalation

Afin de faire fonctionner l'application en locale et contourner la limite de 800 caratère de l'application publique, la marche à suivre est la suivante:
- Créer un environnement virtuel (python3.8 -m venv /path/to/env)
- Activer l'environnement (source /path/to/env/bin/activate)
- Cloner le répertoire (git clone https://github.com/binbin83/passive_detection_app.git)
- Installer les dépendances (pip install -r requirements.txt)
- Vous pouvez désormais utiliser le Notebook *notebook/tuto-exemple.ipynb* ou créer votre propose script.


## 4. Limitations
Notre système de régle possède des limitations: 
- Lorque le participe passé et l'auxiliaure sont inversés : 
> "Plusieurs personnes, dont Pierre Paoli, militant de Corsica libera soupçonné d’avoir été le chef du Front de libération nationale corse (FLNC)"
- La distinction entre le passé composé et la voix passive tronqués n'est pas toujours bien faites:
> "Je suis allé au cinéma", renvoie un passif
- La différence entre les adjectifs  certains participes passés passif n'est pas toujours évidente:
> ex

## 5. To do
Afin de continuer ce projet, il faudrait : 
- Mettre à jour la liste des verbe transitif en Français
- Ajouter la vesion anglaise
- Présenter des performance à partir d'un corpus de référence
- Comparer ces performances à un modèle de type SequenceClassification
