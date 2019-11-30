#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
import plac
import attr
from pathlib import Path
from git import Repo, InvalidGitRepositoryError
from ruamel.yaml import YAML
import pypandoc


@attr.s
class ContentFile():
    source = attr.ib()
    
    def meta_data(self):
        yaml = YAML()
        yaml.explicit_start = True
        yaml.explicit_end = True
        self.metadata = 
    
    
    def write_working_file(self, working_dir):
        outputfile = Path(working_dir, self.
        if self.source is str:
            pypandoc.convert_text(*self.args, **self.kwargs)
        else:
            pypandoc.convert_file(*self.args, **self.kwargs)
    


 


def set_config_file():
    pass
    
def get_git(working_dir):
    try:
        repo = Repo(working_dir)
    except InvalidGitRepositoryError:
        repo = Repo.init(working_dir)
    return repo
    


def extract_content(src):
    if src.isdir():
        for filepath in src.iterdir():
            yield ContentFile(filepath)
    elif src.suffix == 'zip':
        for zip_object in src:
            yield read_file(zip_obj)
    else:
        yield read_file(src)
    return True
    


def main(source):
    repo.checkout('src')
    for content_file in extract_content(Path(source)):
        
        filename = write_content_file(content)
        if not filename in repo.files
            repo.add(filename)
    repo.commit('added source files')
    
        
    
            
   
    
    
if __name__ == '__main__':
    plac.call(main)
