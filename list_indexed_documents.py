#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import re
import fire
from pathlib import Path
from redis import Redis
import uuid


r = Redis(decode_responses=True)

def filter_on_metadata(document_key, match_key, match_value):
    metadata_key = document_key.replace('document', 'metadata')
    metadata_value = r.hget(metadata_key, match_key)
    if type(match_value) is str:
        return re.search(match_value, metadata_value)
    elif type(match_value) is int:
        try:
            return match_value == int(metadata_value)
        except ValueError:
            return False
    else:
        return False

def list_indexed_documents(project, **filterspecs):
    for document_key in r.keys(f'{project}:document:*'):
        if len(filterspecs) == len( [k for k,v in filterspecs.items() if filter_on_metadata(document_key, k, v)]):
            yield document_key

if __name__ == '__main__':
    fire.Fire(list_indexed_documents)
