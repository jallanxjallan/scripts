#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import fire
from pathlib import Path
import sys
import re
import redis
import uuid

r = redis.Redis(decode_responses=True)
pat = re.compile('\W+((\w|\-)+)\s\.section\W')

def split_into_sections():
    def make_doc_keys():
        for no, section in enumerate(sections):
            identifier, content = section
            doc_data['identifier'] = identifier
            doc_data['sequence'] = no
            doc_data['text'] = content

            doc_key = uuid.uuid4().hex
            r.hmset(doc_key, doc_data)
            r.expire(doc_key, 10)
            yield doc_key


    rkey = sys.stdin.read().strip("\n")
    doc_data = r.hgetall(rkey)

    s = re.split(pat, doc_data['text'])
    sections = [(s[i], s[i+2]) for i in range(1,len(s)-1, 3)]

    print('\n'.join([k for k in make_doc_keys()]))

if __name__ == '__main__':
    fire.Fire(split_into_sections)
