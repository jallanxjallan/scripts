#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from attrs import define, field
from pathlib import Path
from collections import Counter
import re
from script_lib import initialize_class, truncate_story_path, Reader, Writer
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
link_counter = Counter()
absentees = []


@define 
class StoryLink(Reader, Writer):
	base_dir = field(converter=Path)
	index_file = field(default='content_index.md')
	doc_dir= field(default='stories', converter=Path)
	
	def check_story_links(self):
		doc = Document.read_file(self.index_file)
		new_content = re.sub(link_pattern, self.update_story_link, doc.content)
		if len(absentees) > 0:
			print(f"{' '.join(absentees)} not found") 
		if max(link_counter.values()) > 1:
			print(f"{' '.join([l for l,i in link_counter.items() if i > 1])} referenced more than once")
		Document(content=new_content).write_file(doc.filepath, overwrite=True)
		
	def update_story_link(self: object, match: object) -> str:
		link_text = match.group(1)  # The text part [link text]
		url = match.group(2)        # The URL part (url)
		if Path(url).exists():
			new_url = truncate_story_path(url) 
			link_counter[str(new_url)] += 1
		else:
			absentees.append(url) 
			link_text = f'{link_text} not found'
		
		return f"[{link_text}]({new_url})"
	
	

def init_class(**kwargs):
	linker = initialize_class(StoryLink, **kwargs)
	linker.check_story_links() 

if __name__ == "__main__":
	fire.Fire(init_class)