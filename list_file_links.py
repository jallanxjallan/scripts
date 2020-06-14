# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import fire
from pathlib import Path
from redis import Redis
from urllib.parse  import urlunparse

r = Redis(decode_responses=True)

base_path = Path.cwd()

def list_file_links(*fields):
    document_keys = [k.strip("\n") for k in sys.stdin.readlines()]
    for document_key in document_keys:
        for key, value in [(k,v) for k,v in r.hgetall(document_key).items() if k in fields]:
            print(key.title(), ':', r.hget(document_key, key) or '-')
        print(urlunparse(('file', str(base_path), r.hget(document_key, 'filepath'), None, None, None)))
        print('=' * 30)

if __name__ == '__main__':
    fire.Fire(list_file_links)
