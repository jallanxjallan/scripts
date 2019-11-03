#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  dispatch_edited_files.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from pathlib import Path
import zipfile
import pypandoc
import plac

def main(edited_files_dirname, container_filename, output_format='rtf'):
    source = Path(edited_files_dirname)
    with zipfile.ZipFile(container_filename, 'w') as container:
        for filepath in source.iterdir():
            try:
                file_data = pypandoc.convert_file(str(filepath), to=output_format, extra_args=['--standalone'])
            except Exception as e:
                print(e)
                continue
            arc_path = filepath.with_suffix(f'.{output_format}')
            container.writestr(arc_path.name, file_data)
    return True

if __name__ == '__main__':
    plac.call(main)
    
