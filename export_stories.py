#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com> 

import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import re
import psutil 
from document import Document
from utility import timestamp, title_case
import subprocess
import fire 

heading_pat = re.compile(r'^\#*\s')


def make_story(notepath, storypath):
	with notepath.open() as np:
		contents = np.readlines() 
		title = heading_pat.sub('', contents.pop(0).strip())
		return Document(content=contents,
				metadata=dict(title=title, status='exported', created=timestamp())
				).write_file(storypath)
		

def main(notes_file, story_dir):

	if any(p.info['name'] == 'cherrytree' for p in psutil.process_iter(['name'])):
		print('cherrytree already running')
		sys.exit(0)
	
	staging_dir = TemporaryDirectory(prefix='story_export', delete=False).name
	command = ['cherrytree', notes_file, '--export_to_txt_dir', staging_dir]
	rs = subprocess.run(command) 
	
	story_path = Path(story_dir)
	staging_path = Path(staging_dir).joinpath(f'{notes_file}_TXT')
	for notepath in staging_path.iterdir():
		basename = notepath.stem
		parts = basename.split('--')
		if not (filepath := story_path.joinpath(parts[-1]).with_suffix('.md')).exists():
			docpath = make_story(notepath, filepath)
			print(f'exported {docpath}')
	

if __name__ == '__main__':
	fire.Fire(main)

