#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
from attrs import define, field
from pathlib import Path
from urllib.parse import urlparse
import regex
import pyperclip
from script_lib import initialize_class
import fire

# pattern = r'\[(?P<label>[^\]]+)\]\((?P<filepath>\/(?:[^\s\/]+\/)*[^\s\/]+)\)'
pattern = regex.compile(r'\[(?<label>[^\]]+)\]\((?<filepath>[^)]+)\)')


@define 
class Linker():
	edit_path = field(default='edits', converter=Path)
	
	def make_edit_links(self):
		context = pyperclip.paste()
		if not pattern.search(context):
			print('No links found in text') 
			sys.exit(0)

		edit_path = self.edit_path
		[l.unlink() for l in edit_path.iterdir() if l.is_symlink] 
		
		for i, match in enumerate(pattern.finditer(context)):
			target_filepath = Path(urlparse(match['filepath']).path).resolve()
			
			if not target_filepath.exists():
				print(f'filepath for {match["label"]} {match["filepath"]} not found')
				continue
			link_filename = f'edit_document_{i:03}' 
			link_filepath = edit_path.joinpath(link_filename).with_suffix('.md').resolve() 
			try:
				link_filepath.symlink_to(target_filepath) 
			except Exception as e: 
				print(f'error making symlink {e}') 
				continue
			
			print(f'Wrote editing link from {target_filepath.name}')  


def init_class(**kwargs):
	linker = initialize_class(Linker, **kwargs)
	linker.make_edit_links() 

if __name__ == "__main__":
    fire.Fire(init_class)