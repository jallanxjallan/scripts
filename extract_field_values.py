#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import fire
from redis import Redis

r = Redis(decode_responses=True)

def extract_field_values(field):
    document_keys = [k.strip("\n") for k in sys.stdin.readlines()]
    for document_key in document_keys:
        try:
            yield r.hget(document_key, field)
        except:
            yield r.get(document_key)

if __name__ == '__main__':
    fire.Fire(extract_field_values)
