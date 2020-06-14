#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import plac
from subprocess import run, PIPE
from redis import Redis
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.append('/home/jeremy/Library')
from utility.helpers import snake_case

project_base = Path('/home/jeremy/Projects')

r = Redis()

def create_project(name):
    project_name = name.lower().replace(' '.'-')
    project_key = f'project:{project_name}'
    
    document_path = cur_dir.joinpath('content', filename)
    redis_key=f'{project}:content:{snake_case(document_path.stem)}'
    args = ['--standalone']
    args.append(f'-o {str(document_path)}')

    with TemporaryDirectory() as tmpdir:
        tmpfile = Path(tmpdir, filename)
        tmpfile.write_text(input())
        args.append(str(tmpfile))
        print(args)

        try:
            rs = run('pandoc', args, universal_newlines=True)
        except Exception as e:
            print (e)
            return False
    print (f'created document {filename}')
    print( redis_key )

if __name__ == '__main__':
    plac.call(create_document)
