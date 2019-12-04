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
from git import Repo, InvalidGitRepositoryError
import git
import dataset







def main(source):
    try:
        repo = Repo(Path.cwd())
    except InvalidGitRepositoryError:
        print('project not initialized')
        return False
    db = dataset.connect(DOCUMENT_INDEX_DB)
    repo = get_repo()
    repo.checkout('src')
    for document in read_documents(source):
        
        filename = write_content_file(content)
        if not filename in repo.files
            repo.add(filename)
    repo.commit('added source files')
    
        
    
            
   
    
    
if __name__ == '__main__':
    plac.call(main)
