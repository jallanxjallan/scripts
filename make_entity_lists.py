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

import pandas as pd
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token
from spacy.lang.en.stop_words import STOP_WORDS

import pypandoc
from textblob import TextBlob
from textblob import Word


from textacy.preprocessing.normalize import normalize_quotation_marks, normalize_whitespace


DF_COLUMNS = ['label', 'entity']

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
    docs = nlp.pipe(content)
    
    entities = []
    words = []
    
    for doc in docs:
        entities.extend([e for e in doc.ents])
        words.extend([t.text for t in doc if filter_token(t) if foreign_word(t)])
    
    df_entities = pd.DataFrame([(e.label_, e.text) for e in entities], columns=['label', 'entity'])
    df_words = pd.DataFrame([(b, 'id') for b in words], columns=['word', 'language'])
    
    with pd.ExcelWriter(outfile) as writer:
        df_entities.drop_duplicates().sort_values(by=['entity']).to_excel(writer, 'entities')
        df_words.drop_duplicates().sort_values(by=['word']).to_excel(writer, 'words')

        writer.save()
    

if __name__ == '__main__':
    plac.call(main)
