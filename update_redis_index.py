#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import datetime
import fire
from pathlib import Path
from redis import Redis
from redis.exceptions import DataError
from ruamel.yaml import YAML
from uuid import uuid4

r = Redis(decode_responses=True)
yaml=YAML()

def get_document_metadata(filepath):
    try:
        rd = yaml.load(filepath.read_text().split('---')[1])
    except Exception as e:
        print(f'{e} on loading {filepath.stem}')
        return False

    metadata = {'filepath':str(filepath)}
    for key, value in rd.items():
        key = key.lower().replace(' ', '_')
        metadata[key] = value

    return metadata

def update_document_index(document_folder):
    for filepath in [f for f in Path(document_folder).iterdir() if f.suffix == '.md']:
        metadata = get_document_metadata(filepath)
        if not metadata:
            continue
        project = metadata.get('project', 'misc')
        document_key = f'{project}:document:{uuid4().hex}'
        r.hmset(document_key, {k:v for k,v in metadata.items() if v})
        r.expire(document_key, 600)
        yield document_key

if __name__ == '__main__':
    fire.Fire(update_document_index)
