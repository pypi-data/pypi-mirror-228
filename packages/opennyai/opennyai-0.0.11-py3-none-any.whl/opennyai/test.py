
from opennyai import Pipeline
from opennyai.utils import Data
from spacy import displacy
from opennyai.ner.ner_utils import ner_displacy_option


#text = open('/Users/prathamesh/Desktop/itat_sample2.txt').read()
#text = open('/Users/prathamesh/tw_projects/OpenNyAI/git_repos/Opennyai/tests/examples/judgement_texts/72703592.txt').read()
text = open('/Users/prathamesh/tw_projects/OpenNyAI/git_repos/Opennyai/tests/examples/judgement_texts/811682.txt').read()

data = Data([text])
pipeline = Pipeline(components=['NER'], use_gpu=False, verbose=True)
results = pipeline(data)
ner_doc = pipeline._ner_model_output[0]


displacy.serve(ner_doc, style='ent',port=8083
               ,options=ner_displacy_option)
# from opennyai import Pipeline
# from opennyai.utils import Data
# import glob
# import json
# import pandas as pd
# import re
# from tqdm.notebook import tqdm
# import spacy
#
# search_results = pd.read_csv(
#     '/Users/prathamesh/tw_projects/OpenNyAI/data/court_search/personal_liberty/search_results_judgment_metadata.csv')
# search_result_dir = '/Users/prathamesh/tw_projects/OpenNyAI/data/court_search/personal_liberty/'
# search_results['judgment_text'] = search_results['judgment_id'].apply(
#     lambda x: open(search_result_dir + 'txt/' + x + '.txt').read())
# files = search_results['judgment_text'].to_list()
# ids = search_results['judgment_id'].to_list()
#
#
# files = []
# ids = []
# nlp = spacy.load('en_core_web_sm')
# for index, row in search_results.iterrows():
#     if len(nlp.tokenizer(row['judgment_text'])) < 100000:
#         files.append(row['judgment_text'])
#         ids.append(row['judgment_id'])
#
# data = Data(input_text=files[:2],file_ids= ids[:2], mini_batch_size=20000)
# data = [i for i in data]
# for i in data:
#     print(i['file_id'])