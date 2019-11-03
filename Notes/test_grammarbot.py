#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
import plac
from pathlib import Path
import textacy
from textacy.preprocessing.normalize import normalize_hyphenated_words, normalize_quotation_marks, normalize_whitespace
from grammarbot import GrammarBotClient
import spacy
from spacy.tokens import Doc, Span, Token

CHUNK_SIZE = 7000

Token.set_extension("typo", default=None)

nlp = spacy.load('en_core_web_sm')
    
client = GrammarBotClient(api_key='KS9C5N3Y')

data_dir = '/home/jeremy/Desktop/rini_makmur/'

def find_token(doc, match):
    for token in doc:
        token_start = len(doc[doc.start:token.i].text)
        token_end = token_start + len(token)
        if token_start < match.replacement_offset < token_end:
            return token
    return None

def check_grammar(doc):
    res = client.check(doc.text)
    for match in res.matches:
        print(match.message)
        token = find_token(doc, match)
        if token:
            print(token.text)
            token._.typo = match.message

def main(text_path, res_path):
    
    
    text = Path(data_dir, text_path).read_text()
    
    doc = nlp(text)
    
    start = 0
    end = 0
    for sent in doc.sents:
        if (len(doc[start:end].text) + len(sent)) > CHUNK_SIZE:
            check_grammar(doc[start:end])
            start = sent.end
            end = sent.end
        else:
            end = sent.end
        
        if start > 2000:
            break 
    output = []
    for token in doc:
        if token._.typo:
            output.append(f'**{token.text}{token._.typo}**')
        else:
            output.append(token.text)
            
    Path(data_dir,  res_path).write_text(' '.join(output))
    

    
if __name__ == '__main__':
    plac.call(main)
