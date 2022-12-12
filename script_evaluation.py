
import pandas as pd

from src.evaluate_parser import clean_data, cut_text, eval_one_doc
from src.PassivePy import PassivePyAnalyzer
from src.analysis_passive import load_model_from_name
from utils import load_config

def main(annotation, analyzer, seuil):
    
    clean_annotation  = clean_data(annotation) # remove double spacing
    clean_annotation['cut_text'] = clean_annotation.apply(cut_text, axis=1) # remove all text after label:  "Fin"

    clean_annotation['n_VP'], clean_annotation['n_true'] , clean_annotation['n_test'], clean_annotation['VP_test'], clean_annotation['FN_errors'], clean_annotation['FP_errors'] = \
        zip(*clean_annotation.apply(lambda x : eval_one_doc(x,analyzer, seuil=seuil), axis=1))
    clean_annotation['recall'] =  clean_annotation['n_VP'] / clean_annotation['n_true']
    clean_annotation['precision'] =  clean_annotation['n_VP'] / clean_annotation['n_test']
    clean_annotation['f1'] =  2 * clean_annotation['recall']  * clean_annotation['precision'] / (clean_annotation['recall'] + clean_annotation['precision'])
    
    return clean_annotation

if __name__ == "__main__":
    config = load_config()
    model_name = config['model_name']
    print(f"The loaded model is {model_name}")
    annotation = pd.read_json(config['annotation_file_path'], lines =True)
    print(f"The annotation file loaded is {config['annotation_file_path']}")
    seuil = config['overlap_seuil']
    print(f"The overlaping seuil for evaluation is set to {seuil} characters")
    
    nlp = load_model_from_name(model_name)
    # load the analyzer
    analyzer =  PassivePyAnalyzer(nlp= nlp)
    
        
    #select sample
    sample = annotation.iloc[:]
    # compute the evaluation table
    sample_evaluated = main(sample, analyzer, seuil=seuil)
    #save the result
    sample_evaluated[['n_test',"n_true","n_VP","VP_test","recall","precision","f1"]].to_csv(f'./error_analysis/{model_name}_evaluation_stats.csv')
    # print the recall and precision
    recall = sample_evaluated['n_VP'].sum()/sample_evaluated['n_true'].sum()
    precision = sample_evaluated['n_VP'].sum()/sample_evaluated['n_test'].sum()
    f1 = 2* recall * precision / (recall + precision)
    result_dict = {"recall":recall, "precision":precision, "f1":f1}
    
    f = open(f"./error_analysis/{model_name}_evaluation_results.txt", "w")
    for score_name, score in result_dict.items() :
        f.write(f'{score_name}: {score};\n')
        print(f'{score_name}: {score};')

    # saving the error by documents
    FP = []
    FN = []
    for i in range(len(sample_evaluated)) :
        fp = sample_evaluated['FP_errors'][i].sort_values("start")
        fp.to_csv(f'./error_analysis/{i}_FP_{model_name}.csv')
        FP.append(fp)
        fn = sample_evaluated['FN_errors'][i].sort_values("start")
        fn.to_csv(f'./error_analysis/{i}_FN_{model_name}.csv')
        FN.append(fn)
    
    df_FP = pd.concat(FP)
    df_FP.to_csv(f'./error_analysis/CONCAT_FP_{model_name}.csv')
    df_FN = pd.concat(FN)
    df_FN.to_csv(f'./error_analysis/CONCAT_FN_{model_name}.csv')
