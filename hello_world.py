#!/home/jeremy/Python3.6Env/bin/python
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

from document import Document


def main():
    doc = Document('hello world')
    print(doc)


if __name__ == '__main__':
    plac.call(main)
