import spacy
from spacy.matcher import Matcher

def create_matcher(spacy_model = "fr_core_news_lg", nlp:spacy.language.Language = None):

    """creates a matcher on the following vocabulary"""
    if not nlp:
        nlp = spacy.load(spacy_model, disable=["ner"])
    matcher = Matcher(nlp.vocab)

    # list of verbs that their adjective form 
    # is sometimes mistaken as a verb
    verbs_list = ["user",'utiliser',"subir"]

    #--------------------------rules--------------------#



    passive_rule_0 = [
        {"POS":"AUX", "DEP": "aux", "OP":"*"},
        {"POS":"AUX", "DEP": "aux:pass", "OP":"+"},
        {"DEP":"neg", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"DEP":"HYPH", "OP":"*"},
        {"DEP":"advmod", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"TAG":"ADV","OP":"*"},
        {"POS":"VERB", "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part","Voice=Pass"]}, "LEMMA":{"NOT_IN" : verbs_list }},
        {"LOWER":"par"}
    ]
    # exemple : J'ai été attaqué par des loups !
    
    passive_rule_1 = [
        {"POS":"AUX", "DEP": "aux", "OP":"*"},
        {"POS":"AUX", "DEP": "aux:pass", "OP":"+"},
        {"DEP":"neg", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"DEP":"HYPH", "OP":"*"},
        {"DEP":"advmod", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"TAG":"ADV","OP":"*"},
        {"POS":"VERB", "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part","Voice=Pass"]}, "LEMMA":{"NOT_IN" : verbs_list }}
    ]

    """
    sentence : The book was read by him.
    dependencies : ['det', 'nsubjpass', 'aux:pass', 'ROOT', 'agent', 'pobj', 'punct']
    Tags : ['DT', 'NN', 'VBD', 'VBN', 'IN', 'PRP', '.']
    """
    passive_rule_2 = [
        {"DEP": {"IN": ["attr", 'nsubjpass', 'appos']}},
        {"TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "DEP": "advmod", "OP" : "*"},
        {"DEP": "PUNCT", "OP" : "*"},
        {"TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part","Voice=Pass"]}, "DEP": "acl","LEMMA": {"NOT_IN" : verbs_list}}
    ]

    """
    sentence : there was no change detected in her behavior.
    dependencies : ['expl', 'ROOT', 'det', 'attr', 'acl', 'prep', 'poss', 'pobj', 'punct']
    tags : ['EX', 'VBD', 'DT', 'NN', 'VBN', 'IN', 'PRP$', 'NN', '.']
    """


    passive_rule_3 = [
        {"POS":"AUX", "DEP": "aux", "OP":"*"},
        {"POS":"AUX", "DEP": "aux:pass", "OP":"+"},
        {"DEP":"neg", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"DEP":"HYPH", "OP":"*"},
        {"DEP":"advmod", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"POS":"VERB", "DEP":"ROOT", "LEMMA":{"NOT_IN" : verbs_list}},
        {"DEP":"cc"},
        {"TAG":"ADV","OP":"*"},
        {"DEP":"advmod", "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part","Voice=Pass"]}, "OP": "*", "LEMMA": {"NOT_IN":["pre"]}},
        {"DEP": "conj", "LEMMA":{"NOT_IN" : verbs_list}},
        {"DEP":"pobj", "OP":"!"}
    ]

    """
    Used for the second part with "et ..." 
    sentence : "elle a été sélectionnée, et entrainée par les meilleurs ! "
    
    """


    passive_rule_4 = [
        {"DEP":{"IN":["advcl","ROOT"]}, "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part","Voice=Pass"]}},
        {"DEP": "case", "TAG":"ADP"},
        {"OP":"*"},
        {"DEP": "obl:agent"},
    ]

    """
    sentence : Accusé par la police, il fut comdané à 5 ans de prison
    dependencies : ['advcl', 'agent', 'det', 'pobj', 'punct', 'nsubj', 'neg', 'ROOT', 'nsubj', 'aux', 'ccomp', 'poss', 'attr']
    tags : ['VBN', 'IN', 'DT', 'NN', ',', 'PRP', 'RB', 'VBD', 'DT', 'MD', 'VB', 'PRP$', 'NN']
    """

    passive_rule_5 = [
        {"DEP": "nsubj"},
        {"DEP": "ROOT"},
        {"DEP": "attr", "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part","Voice=Pass"]}, "LEMMA":{"NOT_IN" : verbs_list}},
        {"DEP": "prep", "TAG":"ADP", "OP":"*"}
    ]

    """
    sentence : Bears are dreamt of in your fantasies!
    dependencies : ['nsubjpass', 'aux:pass', 'ROOT', 'prep', 'prep', 'poss', 'pobj', 'punct']
    tags : ['NNS', 'VBP', 'VBN', 'IN', 'IN', 'PRP$', 'NNS', '.']
    """


    passive_rule_6 = [
        {"LEMMA": {"IN": verbs_list}},
        {"LOWER":"par"}
    ]

    
    """
    to avoid the confusion between the adjective and passive version of specific 
    verbs, we dedicated a new rule to some verbs to be detected when used with 
    an agent (by)

    sentence : Natural resources are exhausted by humans.
    dependencies : ['amod', 'nsubjpass', 'aux:pass', 'ROOT', 'agent', 'pobj']
    tags : ['JJ', 'NNS', 'VBP', 'VBN', 'IN', 'NNS']
    """

    passive_rule_7 = [
        {"TAG":"PRON", "MORPH" : {"IS_SUPERSET": ["Reflex=Yes"]},"OP":"+"}, #un pronom reflexif, facultatif
        {"TAG":"AUX","DEP" : "aux:tense","OP":"*"}, #un auxiliaire de temps
        {"TAG": {"IN":["VERB","AUX"]},"LEMMA":{"IN":["faire","voir"]}}, # verb/aux faire ou voir
        {"TAG":"VERB","MORPH": {"IS_SUPERSET": ["VerbForm=Inf"]}}, # un verbe à l'infinitif
        {"LOWER":"par","OP":"*"} #la proposition "par" qui est facultative
    ]

    passive_rule_8 = [
        {"TAG":"ADJ", "TEXT" : {"REGEX": r"\b(\w*(ible|able|uble))\b"}}, # adjectif se finnissant par ible ou able
    ]
    
    """
    Formes passives factitives
    Dans ce type d’emplois représenté par 45 occurrences, on distinguera essentiellement les
    emplois dits « tolératifs » construits avec le semi-auxiliaire se laisser et les emplois
    proprement « factitifs » construits avec faire et parfois avec (se) voir. Cet emploi rappelle les
    « passifs canoniques » dans la possibilité qu’il a de pouvoir occulter l’agent AR2 ou de
    retarder son apparition :
    on a voulu passer le permis moto donc euh hm oui non mais on s'est fait
    rouspéter hein par lui …
    """



    # ------------------adding rules to the matcher----------#
    matcher.add("passif_canonique", [passive_rule_0], greedy='LONGEST')
    matcher.add("passif_tronqué", [passive_rule_1], greedy='LONGEST')
    matcher.add("passive_rule_2", [passive_rule_2], greedy='LONGEST') # n'exhioste pas en français à priori
    matcher.add("passif_sequencé", [passive_rule_3], greedy='LONGEST')
    matcher.add("passif_impersonel", [passive_rule_4], greedy='LONGEST')
    matcher.add("passive_rule_5", [passive_rule_5], greedy='LONGEST')# n'existe pas en français je pense
    matcher.add("passif_verbale", [passive_rule_6], greedy='LONGEST')
    matcher.add("passif_factif", [passive_rule_7], greedy='LONGEST')
    matcher.add("passif_adjectif", [passive_rule_8], greedy='LONGEST')
    # print('Matcher is built.')

    return nlp, matcher