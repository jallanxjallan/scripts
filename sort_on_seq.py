#!/home/jeremy/Python3.6Env/bin/python
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
import uuid

r = Redis(decode_responses=True)

def get_sequence(document_key):
    metadata_key = document_key.replace('document', 'metadata')
    sequence = r.hget(metadata_key, 'sequence') or 0.0
    print(sequence)
    return float(sequence)

def sort_on_seq():
    sequence_key = f'sequence:{uuid.uuid4().hex}'
    r.expire(sequence_key, 600)
    document_keys = [k.strip("\n") for k in sys.stdin.readlines()]
    r.zadd(sequence_key, {k:get_sequence(k) for k in document_keys})
    for document_key in r.zrangebyscore(sequence_key, '-inf', '+inf'):
        yield document_key


if __name__ == '__main__':
    keys = fire.Fire(sort_on_seq)
