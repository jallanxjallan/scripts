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
from tempfile import mkdtemp
import attr
import subprocess

sys.path.append('/home/jeremy/Library')

from document.yaml_document import load_yaml_from_file, dump_yaml_to_file
from utility.helpers import make_identifier, title_case, snake_case

compile_dir = Path(mkdtemp())

@attr.s
class Defaults():
    defaults = attr.ib()
    metadata = attr.ib(default=None)
    input = attr.ib(default=None)
    output = attr.ib(default=None)
    filepath = attr.ib()
    @filepath.default
    def _random_filepath(self):
         return str(compile_dir.joinpath(make_identifier()).with_suffix('.yaml'))

    def __attrs_post_init__(self):
        if self.metadata:
            if 'metadata' in self.defaults:
                self.defaults['metadata'].update(self.metadata)
            else:
                self.defaults['metadata'] = self.metadata
        if self.input and type(self.input) is list:
            self.defaults['input-files'] = self.input

        elif self.input and type(self.input) is str:
            self.defaults['input-file'] = self.input
        else:
            self.defaults['input-file'] = blank_file

        if self.output:
            self.defaults['output-file'] = self.output
        else:
            self.output = str(compile_dir.joinpath(make_identifier()).with_suffix('.md'))
            self.defaults['output-file'] = self.output

    def save(self):
        try:
            dump_yaml_to_file(self.defaults, self.filepath)
        except Exception as e:
            print(e)
            return None
        return self.filepath


def create_document():
    config = load_yaml_from_file('create_document.yaml')
    doctypes = [k for k in config.keys()]
    for no, dt in enumerate(doctypes):
        print(f'[{no+1}] {dt}')
    i = int(input('Select Document Type: '))
    try:
        doc_type = config[doctypes[i-1]]
    except IndexError:
        print('No doc type for {i}')
        return False
    identifier = make_identifier()
    title = input('Document Title: ')
    folder = doc_type['folder']
    output_file = Path(folder, snake_case(title)).with_suffix('.md')

    if output_file.exists():
        print(input_file, 'already exists')
        return False
    input_file=compile_dir.joinpath(identifier).with_suffix('.md')
    input_file.write_text(sys.stdin.read())

    defaults = Defaults(doc_type['defaults'],
        input=str(input_file),
        output=str(output_file),
        metadata=dict(title=title, identifier=identifier)
    )
    defaults_file = defaults.save()
    subprocess.run(['pandoc', f'--defaults={defaults_file}'])
    output_url = Path(Path.cwd(), output_file)
    print(f'file://{output_url}')

if __name__ == '__main__':
    fire.Fire(create_document)
