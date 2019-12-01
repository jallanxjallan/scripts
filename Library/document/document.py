#!/home/jeremy/Scripts/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import attr

from ruamel.yaml import YAML
import pypandoc

@attr.s
class Document():
    text = attr.ib()
    source = attr.ib
    x = attr.ib(metadata={'my_metadata': 1})
>>> attr.fields(C).x.metadata
mappingproxy({'my_metadata': 1})
>>> attr.fields(C).x.metadata['my_metadata']
1

Metadata is not used by attrs, and is meant to enable rich functionality in third-party libraries. The metadata dictionary follows the normal dictionary rules: keys need to be hashable, and both keys and values are recommended to be immutable.
    
    def __str__(self):
        return self.text
    
    
    
    
    #~ def write_working_file(self):
        #~ outputfile = Path(Path.cwd(), self.source)
        #~ if self.source is str:
            #~ pypandoc.convert_text(*self.args, **self.kwargs)
        #~ else:
            #~ pypandoc.convert_file(*self.args, **self.kwargs)
