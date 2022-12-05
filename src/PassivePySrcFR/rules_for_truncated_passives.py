import spacy
from spacy.matcher import Matcher


def create_matcher_truncated(nlp:spacy.language.Language = None):

    """creates a matcher on the following vocabulary"""

    matcher = Matcher(nlp.vocab)


    # list of verbs that their adjective form 
    # is sometimes mistaken as a verb
    verbs_list = ["user",'utiliser',"subir"]

    #--------------------------rules--------------------#

    
    passive_rule_1 = [
        {"POS":"AUX", "DEP": "aux", "OP":"*"},
        {"POS":"AUX", "DEP": "aux:pass", "OP":"+"},
        {"DEP":"neg", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"DEP":"HYPH", "OP":"*"},
        {"DEP":"advmod", "TAG":"ADV","MORPH": {"IS_SUPERSET": ["Degree=Pos"]}, "OP":"*"},
        {"POS":"VERB", "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part"]}, "LEMMA":{"NOT_IN" : verbs_list + ['be']}},
        {"DEP":"agent", "OP":"!"}
    ]

    """
    sentence : The book was read by him.
    dependencies : ['det', 'nsubjpass', 'aux:pass', 'ROOT', 'agent', 'pobj', 'punct']
    Tags : ['DT', 'NN', 'VBD', 'VBN', 'IN', 'PRP', '.']
    """
    passive_rule_2 = [
        {"DEP": {"IN": ["attr", 'nsubjpass', 'appos']}},
        {"TAG": "RB", "DEP": "advmod", "OP" : "*"},
        {"DEP": "PUNCT", "OP" : "*"},
        {"TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part"]}, "DEP": "acl","LEMMA": {"NOT_IN" : verbs_list}},
        {"DEP":"agent", "OP":"!"}
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
        {"DEP":"advmod", "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part"]}, "OP": "*", "LEMMA": {"NOT_IN":["pre"]}},
        {"DEP": "conj", "LEMMA":{"NOT_IN" : verbs_list}},
        {"DEP":"pobj", "OP":"!"}
    ]

    """
    Used for the second part with "and ..." 
    sentence : it was determined and formed.
    dependencies : ['nsubjpass', 'aux:pass', 'ROOT', 'cc', 'conj', 'punct']
    tags : ['PRP', 'VBD', 'VBN', 'CC', 'VBN', '.']
    """


    passive_rule_5 = [
        {"DEP": "nsubj"},
        {"DEP": "ROOT"},
        {"DEP": "attr", "TAG":"VERB","MORPH": {"IS_SUPERSET": ["Tense=Past","VerbForm=Part","Voice=Pass"]}, "LEMMA":{"NOT_IN" : verbs_list}},
        {"DEP": "prep", "TAG":"ADP", "OP":"*"},
        {"DEP":"agent", "OP":"!"}
    ]

    """
    sentence : Bears are dreamt of in your fantasies!
    dependencies : ['nsubjpass', 'aux:pass', 'ROOT', 'prep', 'prep', 'poss', 'pobj', 'punct']
    tags : ['NNS', 'VBP', 'VBN', 'IN', 'IN', 'PRP$', 'NNS', '.']
    """



    # ------------------adding rules to the matcher----------#

    matcher.add("passive_rule_1", [passive_rule_1], greedy='LONGEST')
    matcher.add("passive_rule_2", [passive_rule_2], greedy='LONGEST')
    matcher.add("passive_rule_3", [passive_rule_3], greedy='LONGEST')
    matcher.add("passive_rule_5", [passive_rule_5], greedy='LONGEST')

    # print('Matcher is built.')

    return matcher
