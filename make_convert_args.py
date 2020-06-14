#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import fire
from pathlib import Path
import redis
import uuid

r = redis.Redis()

base_dir = Path.cwd()

def make_convert_args(source, destdir, filetype):
    rkey = uuid.uuid4().hex
    r.expire(rkey, 10)

    for filepath in [f for f in sys.stdin.read()]:
        r.hset(rkey, 'sourcepath', str(base_dir.joinpath(filepath)))
        r.hset(rkey, 'destpath', str(base_dir.joinpath(destdir)))
    print(rkey)

if __name__ == '__main__':
    fire.Fire(make_convert_args)
