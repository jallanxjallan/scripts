#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import csv
from pathlib import Path
import plac
from collections import defaultdict

import pandas as pd
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token

import pypandoc



from textacy.preprocessing.normalize import normalize_quotation_marks, normalize_whitespace


DF_DEFS = dict(
    entity=dict(sheet='Entities', columns=['label', 'entity', 'new_label', 'normalize']),
    term=dict(sheet='Terms', columns=['term', 'format', 'normalize']),
    phrases=dict(sheet='Noun Phrases', columns=['phrase', 'format'])
    )


def extract_content_from_file(filename):
    fn = Path(filename)
    if fn.suffix in ['md', 'txt']:
        text = source_file.read_text()
    else:
        text = pypandoc.convert_file(filename, to='markdown_mmd')
    t1 = normalize_whitespace(text)
    return normalize_quotation_marks(t1)
        
def filter_token(t):
    if t.is_stop:
        return False
    if t.is_punct:
        return False
    if t.ent_type > 0:
        return False
    if t.is_digit:
        return False
    if t.is_upper:
        return False
    if  t.ent_type:
        return False
    if not t.pos_ in ['NOUN', 'ADJ']:
        return False
    return True
    
def foreign_word(t):
    w = Word(t.text)
    if len(w.synsets) > 0:
        return False
    return True
        
def main(outfile, *sources):
    
    content = []
    
    for source in sources:
        sfn = Path(source)
        if len(source) > 128:
            content.append(source)
        
        elif sfn.is_file():
            content.append(extract_content_from_file(source))
        
        elif sfn.is_dir():
            for filename in os.listdir(source):
                content.append(extract_content_from_file(filename))
        else:
            print('dont know what to do')
            return
    
    
    nlp = spacy.load('en_core_web_sm')
    
    
    data = defaultdict(list)
    dfs = defaultdict(dict)
    
    
    for doc in nlp.pipe(content):
        data[DF_DEFS['entity']['sheet']].extend([e for e in doc.ents])
        data[DF_DEFS['phrase']['sheet']].extend([p for p in doc.noun_phrases])
        data[DF_DEFS['term']['sheet']].extend([t.text for t in doc if filter_token(t)])
        
    for key, value in data.items():
        name = DF_DEFS[key]['sheet']
        columns = DF_DEFS[key]['columns']
        dfs['new'][name] = pd.DataFrame(item, columns=columns)
        
    if Path(outfile).exists():
        df_entities = pd.read_excel(outfile, sheet_name = ENTITY_SHEET)
        df_terms = pd.read_excel(outfile, sheet_name = TERM_SHEET)
    else:
        df_entities = pd.DataFrame([], columns=ENTITY_COLUMNS)
        df_terms = pd.DataFrame([], columns=TERM_COLUMNS)
        
    df_entities.merge(
        
    
    df_entities = pd.DataFrame([('x', e.label_, e.text) for e in entities], columns=ENTITY_COLUMNS).drop_duplicates()
    df_terms = pd.DataFrame([('x', t, ) for t in terms], columns=TERM_COLUMNS).drop_duplicates()
    
    with pd.ExcelWriter(outfile) as writer:
        df_entities.sort_values(by=['entity']).to_excel(writer, 'entities')
        df_words.sort_values(by=['term']).to_excel(writer, 'terms')

        writer.save()
    

if __name__ == '__main__':
    plac.call(main)
