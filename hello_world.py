#!/home/jeremy/Scripts/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
import plac
from pathlib import Path


sys.path.append('/home/jeremy/Scripts/Library')

from document.text_document import text_to_file


def main(name, filepath):
    Path(filepath).write_text(f'Hello World from {name}')
    print('finished')


if __name__ == '__main__':
    plac.call(main)
