""" 
Copy of the file: https://github.com/mitramir55/PassivePy/blob/main/PassivePyCode/PassivePySrc/rules_for_all_passives.py
Supression des options concernant le passif tronqué  et passif complet
Ajout d'une fonction pour visualiser dans Displacy
"""

import pandas as pd
import numpy as np
import spacy
from termcolor import colored
import re
from itertools import chain 
import os, sys


try: 
    from src.rules_for_all_passives import create_matcher
except: 
    from rules_for_all_passives import create_matcher




class PassivePyAnalyzer:
    
        """
            Get the data from a dataframe.

            Clean the dataset based on the given regex patterns.
            Match passive voice sentence level or corpus level.
            save the output to a file

        """
        def __init__(self, nlp:spacy.language.Language=None, spacy_model:str = "en_core_web_lg"):

            """
            Create the Detector

            n_processses: number of core to use
            batch_size: size of batches of records passed onto the matcher
            regex_patterns: Patterns that should be detected and cleaned from the data
            
            
            """
            self.nlp, self.matcher = create_matcher(nlp=nlp, spacy_model=spacy_model)
            

        def print_matches(self, sentence):
            """
            prints match span - I removed this from parse_sentence after changing its 
            structure. It is used by the author for testing.
            """
            doc = self.nlp(sentence)
            matches = self.matcher(doc)

            samples = []
            if matches:
                for id_, s,e in matches:
                    match_ = doc[s:e] 
                    print(match_)
                    print(colored('rule: ', 'blue'), self.nlp.vocab.strings[id_])
                    samples.append((s,e,self.nlp.vocab.strings[id_],match_))
            else: print('No match.')

            return samples

        def prepare_visualisation(self,sentence):
            doc = self.nlp(sentence)
            matches = self.matcher(doc)


            if matches:
                spans_list = []
                for id_, s,e in matches:
                    span = doc[s:e]
                    span.label_ = self.nlp.vocab.strings[id_]
                    spans_list.append(span)
                doc.spans["passive"] = spans_list
                return matches, doc

            else : 
                return matches, doc    
       

        def parse_sentence(self, sentence):
            """
            This function allows us to see the components of a sentence, 
            specifically, the POS, DEP, and lemma
            """
            doc = self.nlp(sentence)

            df_output = pd.DataFrame(
                index=['POS', 'dependency', 'tag', 'lemma',"moprh"]
                )

            for token in doc:
                df_output.loc[:, token.text] = [token.pos_,
                    token.dep_, token.tag_, token.lemma_, token.morph]
                    
            return df_output


        def _detect_sents(self, document, batch_size, n_process):

            print('Detecting Sentences...')

            """
            Separates sentences from each other in each record
             and puts them in a list along side the count of sentences in each 
             document in another list
             """
            # document = [corpus.lower() for corpus in document]

            all_sentences = []
            count_sents = []

            # go through all the records
            m = 0
            for record_doc in self.nlp.pipe(document, batch_size=batch_size, n_process = n_process):


                sentences = list(record_doc.sents)
                sentences = [str(sentence) if len(sentence)>=2 else 'Not a Sentence' for sentence in sentences] 


                unwanted = []
                for sentence in sentences:
                    i = sentences.index(sentence)
                
                    
                    #...........................joining with the previous one.............................#
                    # ones that start with but and their previous record doesn't have dot at its end
                    if i!=0:
                        if (re.search(r'^ *mais', sentence) and not re.search(r'.$', sentences[i-1])) or all((re.search(r'^[A-Z0-9]', word) or re.search(r'^[\(\)\.\-]', word)) for word in sentence.split()) or re.search(r'^\(.*\)[\.\!\,]*', sentence):
                            j = 0
                            for j in range(1, i):
                                if i-j not in unwanted:
                                    sentences[i-j] = sentences[i-j] + sentences[i]
                                    unwanted.append(i)
                                    break
                            

                    #.........................joining with the next one..........................#
                    if i != len(sentences)-1:


                        if re.search(r', *$', sentence): # remove the one that's ended with comma
                            sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                            unwanted.append(i+1)

                        if re.search(r'\- *$', sentence): 
                            # see if it's ended with hyphen then look at the next one
                            # if it has and in the beginning, forget about this one and go to the next to analyze the and 
                            # and not duplicate the process
                            if re.search(r'^ *(\([\w\. ]*\))* *and', sentences[i+1]):
                                continue
                            else: 
                                # but if there was no and in the next one,
                                #  join this with the next

                                sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                                unwanted.append(i+1)
                        # see if it ends with and and join it with the 
                        elif re.search(r'et *$', sentence):
                            sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                            unwanted.append(i+1)

             

                        # end with the following phrases and join with the next ones
                        elif re.search(r'((Exp\.)|(e\.g\.)|(i\.e\.))$', sentence):
                            sentences[i] = ' '.join([sentences[i], sentences[i+1]])
                            unwanted.append(i+1)


                m+=1
                for index in sorted(set(unwanted), reverse=True):
                    del sentences[index]


                count_sents.append(len(sentences))
                all_sentences.append(sentences) 

            all_sentences = list(chain.from_iterable(all_sentences))
            # print(f'Total number of sentences = {len(all_sentences)}')


            return np.array(count_sents, dtype='object'), np.array(all_sentences, dtype='object')


        def _find_doc_idx(self, count_sents):

            """ finds the indices required for the documents and sentences"""

            m = 1
            sent_indices = []
            doc_indices = []
            for i in count_sents:
                n = 1
                for j in range(i):
                    sent_indices.append(n)
                    doc_indices.append(m)
                    n+=1
                m+=1

            return pd.DataFrame(sent_indices), pd.DataFrame(doc_indices)


        def _add_other_cols(self, df, column_name, count_sents):

            """ creates a dataframe of all the other columns
            with the required number of repetitions for each """

            # create a list of all the col names
            fields = df.columns.tolist()
            # remove column_name
            del fields[fields.index(column_name)]

            other_columns = {}
            # create a df of all the other cols with 
            # appropriate number of repetitions
            for col in fields:
                properties = []
                for i in range(len(count_sents)):
                    properties.append(count_sents[i]*[df.loc[i, col]])
                
                properties = list(chain.from_iterable(properties))
                other_columns[col] = properties

            df_other_cols = pd.DataFrame.from_dict(other_columns)

            return df_other_cols  


        def match_text(self, document):

            """ 
            This function finds passive matches in one sample sentence
            """

            # we don't want to print the usual statements
            with HiddenPrints():
                
                df_output = self.match_corpus_level(
                        pd.DataFrame({'text': [document]}), 
                        column_name='text',
                        n_process = 1,
                        batch_size = 1000, 
                        add_other_columns=False,
                        )

                return df_output

                
        def _find_unique_spans(self, doc) ->list:

            """"
            finds matches and checks for overlaps
            """

            final_matches_i = []
            matches_i = self.matcher(doc)

            if matches_i:
                spans = [doc[s:e] for id_, s,e in matches_i]

                for span in spacy.util.filter_spans(spans):
                    final_matches_i.append(str(span))
            return final_matches_i


        def _find_matches(self, sentences, batch_size, n_process) -> dict:

            """ finds matches from each record """
            print(colored('Starting to find passives...', 'green'))  

            # defining the parameters ---------------------------------------
            # all passives parameters
            all_passives_count = []
            all_passives = []
            binary = []

            
            # -----------------------------------------------------------------


            
            for doc in self.nlp.pipe(sentences, batch_size=batch_size, n_process=n_process):

                
                binary_i = 0

                

                                       
                # all passive voices ----------------------------------------------
                matches_i = self._find_unique_spans(doc)
                if matches_i != []:
                    binary_i = 1
                    binary.append(binary_i)
                    all_passives.append(matches_i)
                    all_passives_count.append(len(matches_i))

                # if there were no matches
                else:
                    all_passives.append(None)
                    all_passives_count.append(0)
                    binary.append(binary_i)



            output_dict = {}

            # add columns -------------------------------------------------------
            columns = [sentences, all_passives, all_passives_count, binary]
            

            for element in columns:
                # name of variables will be the name of columns 
                element_name = [k for k,v in locals().items() if v is element][0]
                output_dict[str(element_name)] = pd.Series(element, dtype='object')
            
            return output_dict


        def match_sentence_level(self, df, column_name, n_process = 1,
                                batch_size = 1000, add_other_columns=True):
                                
            """
            Parameters

            column_name: name of the column with text
            level: whether the user wants corpus level or sentence level results
            n_process: number of cores to use can be any number
            between 1 and the maximum number of cores available
            (set it to -1 to use all the cores available)
            batch_size: give records in batches to the matcher
            record when passed
            add_other_columns: True\False whether or not to add the other columns 
            to the outputted dataframe
            """
            
            df = df.reset_index(drop=True)
            # create a list of the column we will process
            document = df.loc[:, column_name].values.tolist()

            # seperating sentences
            count_sents, all_sentences = self._detect_sents(document, batch_size, n_process)

            # create a df of matches -------------------------------------------
            output_dict = self._find_matches(
                all_sentences, batch_size, n_process,
                )
            df_output = pd.DataFrame(output_dict)

            # find indices required for the final dataset based on the document and sentence index
            sent_indices, doc_indices = self._find_doc_idx(count_sents)
            
            # add indices
            df_output.insert(0, "docId", doc_indices)
            df_output.insert(1, "sentenceId", sent_indices)


            # concatenating the results with the initial df -------------------
            if len(df.columns) == 1: 
                add_other_columns=False
            if add_other_columns:

                other_cols_df = self._add_other_cols(df, column_name, count_sents)
                assert len(other_cols_df) == len(df_output)
                df_output = pd.concat([df_output, other_cols_df], axis = 1)
            return df_output


        def _all_elements_in_one_list(self, series_: pd.Series(list)) -> list:
            """
            a function for reducing the size of a series
            """
            # output: 1d list
            passive_matches = [val for val in series_ if val!=None]
            passive_matches = list(chain.from_iterable(passive_matches))
            return passive_matches


        def match_corpus_level(self, df, column_name, n_process = 1,
            batch_size = 1000, add_other_columns=True):

            """
            finds matches based on sentences in all records

            Parameters

            column_name: name of the column with text
            level: whether the user wants corpus level or sentence level
            results
            n_process: number of cores to use can be any number
            between 1 and the maximum number of cores available
            (set it to -1 to use all the cores available)
            batch_size: give records in batches to the matcher
            record when passed
            add_other_columns: True\False whether or not to add the other columns 
            to the outputted dataframe
            sentences to the output dataset

            passive_sents_count: the percentage of sentences with passive in them
            """
            
            df = df.reset_index(drop=True)
            # create a list of the column we will process
            document = df.loc[:, column_name].values.tolist()


            df_output = self.match_sentence_level(
                df, column_name, n_process,
                batch_size, add_other_columns
                )

                     
            
            # all passives
            all_passives = []
            passive_count = []
            binary = []
            passive_percentages = []
            passive_sents_count = []
            # -------------------------------------------------------------------

            # general
            count_sents = []
            output_dict = {}
            columns = [
                document, count_sents, all_passives, passive_count, 
                passive_sents_count, passive_percentages, binary
                ]

            # list all the docs
            ids_ = df_output.docId.unique()
            

            for i in ids_:

                # select all the sentences of a doc
                rows = df_output[df_output['docId'] == i]

                # concatenate all the properties ------------------------------------
                count_sents.append(len(rows))

                # all_passives 
                count_passive_s = sum(rows.binary)
                passive_sents_count.append(count_passive_s)
                passive_percentages.append(count_passive_s/ len(rows))

                # binary will be =1 if there is even one 1 
                if any(rows.binary) == 1: binary.append(1)
                else: binary.append(0)

                # put all matches in one list
                all_matches = self._all_elements_in_one_list(rows['all_passives'].values)
                all_passives.append(all_matches)
                passive_count.append(len(all_matches))

            # put all properties in a df ------------------------------------------------------
            
            for element in columns:
                # name of variables will be the name of columns 
                element_name = [ k for k,v in locals().items() if v is element ][0]
                output_dict[str(element_name)] = pd.Series(element, dtype='object')

            df_output = pd.DataFrame(output_dict)
               
            # add other columns in the initial df -------------------------------------------
            if len(df.columns) == 1: 
                add_other_columns=False

            if add_other_columns:
                
                # create a list of all the col names
                fields = df.columns.tolist()

                # remove column_name
                del fields[fields.index(column_name)]

                assert len(df[fields]) == len(df_output)
                df_output = pd.concat([df_output, df[fields]], axis = 1)
            
            return df_output

# for stopping the print statements in one sample sentences
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
