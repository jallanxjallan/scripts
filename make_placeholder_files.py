#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from attrs import define, field
from pathlib import Path
import re
from script_lib import initialize_class, Reader, Writer
from document import Document
import fire

"""
	Finds all local file links in the markdown content, modifies the URLs, and replaces them.
	
	Args:
		md_content (str): The original markdown content.
		
	Returns:
		str: The modified markdown content with updated URLs.
"""
# Regular expression to find markdown links [link text](url)
link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'  # Matches [text](url)


@define 
class PlaceHolder(Reader, Writer):
	base_dir = field(converter=Path)
	index_file = field(default='content_index.md')
	doc_dir= field(default='stories', converter=Path)
	
	  
	def make_placeholder_files(self):
		doc = Document.read_file(self.index_file)
		new_content = self.find_and_replace_note_refs(doc.content)
		Document(content=new_content).write_file(overwrite=True)
		
	def find_and_replace_note_refs(self: object, md_content: str) -> str:
	
		# Define a function to replace the URL if it's a local link
		def replace_local_link(match):
			link_text = match.group(1)  # The text part [link text]
			url = match.group(2)        # The URL part (url)

			# Check if it's a local file link (no http/https)
			if re.search(r'\.ctd', url):
				# Modify the local URL
				placeholder_link = self.write_placeholder(url)
				# Return the modified markdown link
				return f"[{link_text}]({placeholder_link})"
			else:
				# If it's already a file link return as is
				return match.group(0)
	
		# Use re.sub to replace all matching links in the markdown content
		return re.sub(link_pattern, replace_local_link, md_content) 

	
	def write_placeholder(self: object, note_ref: str) -> str:
		self.note(note_ref)
		self.content = ['Text will go here']
		self.metadata['status'] = 'placeholder'
		try:
			rs = self.write() 
		except FileExistsError:
			print(f'made link to existing file {rs}') 
		else:
			print(f'made placeholder file {rs}')

def init_class(**kwargs):
	linker = initialize_class(PlaceHolder, **kwargs)
	linker.make_placeholder_files() 

if __name__ == "__main__":
	fire.Fire(init_class)