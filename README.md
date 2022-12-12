[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://passive-fr.streamlit.app/)

# Détection de la voix passive dans le Français parlé





- [0. A propos](#0-a-propos)
- [1. Prérequis sur le passif en français](#prérequis-sur-le-passif-en-français)
- [2. Fonctionnement de l'application](#2-fonctionnement-de-lapplication)
- [3. Instalation](#3-instalation)
- [4. Limitations](#4-limitations)
- [5. Ressources sur le passif en Français](#5-ressources-sur-le-passif-en-français)
- [6. Evaluation](#6-evaluation)
- [7. To do](#5-to-do)

## 0. A propos
Cette application permet de détecter la voix passive dans un texte en Français. 

Le code source s'inspire en grande partie de ce projet : <a href = "https://github.com/mitramir55/PassivePy"> PassivePy</a>

L'application publique streamlit associée est disponible en ligne:   <a href = "https://passive-fr.streamlit.app/"> lien streamlit</a> 


Auteur:
- <a href="https://www.linkedin.com/in/robin-quillivic/">Robin Quillivic</a>, Doctorant  (1A)  EPHE - Institut des Systèmes Complexes
- L'annotation des données d'évaluations et l'analyse des erreurs a été réalisé avec <a href="http://www.ddl.cnrs.fr/Annuaires/Index.asp?Langue=en&Page=Frederique%20GAYRAUD ">Frédérique Gayraud</a>

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
- Vous pouvez désormais utiliser le Notebook *notebook/tuto-exemple.ipynb* ou créer votre propre script.
- Vous pouvez également utiliser l'application en local en utilisant :  streamlit run main.py
- Remarque: Si vous souhaitez industrialiser ce code, il faudra penser à optimiser le code. Par exemple réduire la (longue) liste de verbe intransitif qui est testé plusieurs fois par appel.


## 4. Limitations
Notre système de régle possède des limitations: 
- Lorque le participe passé et l'auxiliaure sont inversés : 
> "Plusieurs personnes, dont Pierre Paoli, militant de Corsica libera soupçonné d’avoir été le chef du Front de libération nationale corse (FLNC)"
- La distinction entre le passé composé et la voix passive tronqués n'est pas toujours bien faites. Nottament dans les cas ou les verbes associées peuvent être transitifs et intrnasitifs selon le contexte:
> "J'étais crevé"
- La différence entre les adjectifs  certains participes passés passif n'est pas toujours évidente:
> "La porte est ouverte", "Elle est maquillée"
- Certaines règles ont été adapté à notre corpus qui est un corpus orale. Nous vous conseillons d'anoter une petite partie de votre texte en utilisant Doccano par exemple et de vérifier si les scores sont bons (>80%).

## 5. Ressources sur le passif en Français

La notion de voix passive est complèxe et soulève de nombreux débat au sein de la communauté des linguistes. Nous nous sommes inspiré des ressources suivantes pour développer ce travail :

- La passif à l'oral:  https://hal.archives-ouvertes.fr/halshs-01465258/ 
- Les adjectifs en -able, -ible et -uble: https://www.persee.fr/doc/lfr_0023-8368_1990_num_87_1_6325
- La différences entre adjectifs et passifs: http://kops.uni-konstanz.de/handle/123456789/17583


## 6. Evaluation
Afin de vérifier la pertinence, de notre moteur de régles, nous avons annoté 25 retranscriptions de témoignages, ce qui représente environ 2350 étiquettes passifs sur un corpus d'environ 350 000 mots. **Pour des raisons de confidentialité, nous ne pouvons pas paratger nos données**. Les données nécessaires à l'évaluation doivent être au format jsonl et le chemin foit être changé dans le fichier de config : *config_evaluation.yaml*.  Voici, quelques remarques sur l'annotation des documents : 

- **Difficultés de codage**
    - 1.1. il y a eu des cas d’ambiguïté entre participe passé et adjectifs, notamment avec le terme « blessé » : Nous avons pris le parti de ne le considérer comme un passif que lorsque le terme était employé avec l’auxiliaire être comme en (1), mais de ne l’ai pas codé comme passif dans les cas comme (2) ou (3). Ce choix est discutable, et l’on pourrait décider de coder toutes les occurrences de « blessé » comme des passifs.
            (1) Mon ami a été blessée
            (2) Il y avait partout des personnes blessées
            (3) Les blessés attendaient dans la cour
    
    - 1.2. Concernant les adjectifs en -ble, même si historiquement ils avaient tous un sens passif, il nous semble qu’un certain nombre ne sont plus interprétés comme tel, aussi, avons-nous (subjectivement) exclu les adjectifs suivants :
        Agréable, capable/incapable, sensible / hypersensible, horrible, flexible, possible/impossible, pénible, terrible, disponible, coupable, adorable, aimable, responsable, inconfortable, formidable, instable, raisonnable, exécrable, indispensable, variable

- **Perfomances:** Nous obtenons les performances suivantes, le modèle basé sur transformer bien que beaucoup plus long permet d'augmenter significativement  la précision.

>| Modèle | Rappel | Précision | f1 score |
>|:------:|:------:|:---------:|:--------:|
>| spacy large |  0.84 | 0.70  | 0.77 |
>| spacy trf   |  0.89 | 0.85  | 0.86 |



## 7. To do
Afin de continuer ce projet, il faudrait : 
- [x] Mettre à jour la liste des verbes intransitifs en Français
- [x] Présenter des performances à partir du corpus d'étude
- [ ] Ajouter la version anglaise
- [ ] Présenter des performances à partir d'un corpus de référence
- [ ] Comparer ces performances à un modèle de type SequenceClassification (spacy NER)
