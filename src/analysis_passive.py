""" 
Author: Quillivic Robin
created_at : 2022, 15th Nov
"""

import numpy as np
import pandas as pd

from src.PassivePySrcFR.PassivePy import PassivePyAnalyzer



def load_passive_features(data:pd.DataFrame, analyzer:PassivePyAnalyzer):
    # verify there are not double spacing that makes spacy going mad
    data['text'] = data['text'].apply(lambda x : x.replace("  "," "))
    #compute all passive form in the corpus (might take a while)
    df = analyzer.match_corpus_level(data, 'text', n_process = -1,
            batch_size = 50, add_other_columns=True,
             truncated_passive=True, full_passive=True)
    df['text']  =  df['document']
    
    cols_passive  = ['count_sents', 'all_passives', 'passive_count',
       'passive_sents_count', 'passive_percentages', 'binary',
       'full_passive_matches', 'full_passive_count',
       'full_passive_sents_count', 'full_passive_percentages',
       'binary_full_passive', 'truncated_passive_matches',
       'truncated_passive_count', 'truncated_passive_sents_count',
       'truncated_passive_percentages', 'binary_truncated_passive']

    return df, cols_passive


def load_from_text(text:str,analyzer:PassivePyAnalyzer) -> pd.DataFrame :
    """Returns the passive feature from the text

    Args:
        text (str): _description_
        analyzer (PassivePyAnalyzer): _description_

    Returns:
        pd.DataFrame: _description_
    """

    result = analyzer.match_text(text)

    return result.T

ex_passive = ["elle a été déterminée et formée ! ",
"accusé par la police, il fut condamné a 5 ans de prison ferme"
,"ma mère a été élevée par une euh une une vieille dame euh à euh dans l'Allier"
,"puis on a été soutenu par un monsieur aussi c'est monsieur NPERS…",
"la la République du Centre a été rachetée euh par un journal euh je voudrais pas dire de bêtises je crois que c'est Clermont-Ferrand Clermont enfin…",
"alors il y a des écoles qui sont faites exclusivement par des religieuses ou certains par des prêtres mais alors maintenant ils ont beaucoup d'institutrices euh civiles qui sont dedans",
"donc il est il est payé quoi bah c'est super",
"à à mon avis ça a déjà été fait mais au niveau euh professionnel au niveau du travail je crois que ça se développe ouais",
"quand tu habites dans le centre d'Orléans euh c'est quand même réservé à un public qui a … un minimum d'argent",
"parce que même avant on a été coincé euh pendant pas mal d'années euh sans voiture et on travaillait pas","tu es à peine payé et tout quoi",
"tout à l'heure j'avais été inter- la dernière fois que j'avais été interviewée c'était pour la la construction de la nouvelle fac",
"donc vous êtes  envoyée ponctuellement sur des sur des sur des sites sites",
"d'accord je devais pas rester à Orléans je devais juste être formée pendant un an et partir sur Lille",
"je trouve que pour le moment euh c'est pas encore trop bien aménagé euh pour les vélos hein vélos",
"Les adultes quand tu habites dans le centre d'Orléans euh c'est quand même réservé à un public qui a hm ouais ouais bien sûr ouais un minimum d'argent"
"des  des échanges qui qui se font pas par téléphone",
"on a voulu passer le permis moto donc euh hm oui non mais on s'est fait rouspéter hein par lui",
"Deux matins de suite qu'on se fait réveiller par la perceuse hein",
"non mais il faut réussir à se faire respecter c'est ça le plus dur",
"oui oui y aura toujours des professeurs qui se feront chahuter par leurs élèves",
"genre euh genre si tu te fais je te le souhaite pas ah si tu te fais larguer par ton copain … tu vas dire ah c'est chips"
"c'est que euh tu peux pas te balader euh tranquille quoi tu te fais emmerder par euh par un … par un tas de gens"
"il a été fait toute une série de réformes euh successives hâtives euh non raisonnées non efficaces et finalement l'ensemble du pays était mécontent",
"il a été décidé de qu'on soit transféré dans l'autre école av- avec l'idée de faire une école maternelle primaire commune",
"il a été décidé au niveau national de faire une enquête des de toutes ces industries pour euh savoir d'où venait la source",
"cet espace est resté vacant… pendant longtemps sauf les fêtes de la musique… il a été demandé de pouvoir l’utiliser"
]