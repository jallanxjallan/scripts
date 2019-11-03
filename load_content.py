#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from pathlib import Path
from lxml import etree
from lxml.etree import XMLSyntaxError
import pandas as pd



icml_source_dir = '/home/jeremy/Desktop/cergam/exported_content'
data_file = '/home/jeremy/Desktop/cergam/icml_data.pkl'


def main():
    contents = []
    for filename in os.listdir(icml_source_dir):
        try:
            tree = etree.parse(os.path.join(icml_source_dir, filename))
        except XMLSyntaxError:
            continue
        for e in tree.findall('.//Content'): 
            contents.append((filename, e.getparent().attrib['AppliedCharacterStyle'], e.text))
        
    df = pd.DataFrame(contents, columns=['filename', 'style', 'text'])
    print(df.head())
    df.to_pickle(data_file)
    
    

if __name__ == '__main__':
    main()
    
