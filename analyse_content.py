#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import os
import sys
from attrs import define, field
from script_lib import Analyser, initialize_class
from pathlib import Path
from storage import CherryTree
import fire 

import sys
from pathlib import Path
import regex
from utility import snake_case


from pathlib import Path
import regex
from document import Document
import pandas as pd
from functools import wraps

# Regex pattern to capture markdown file links
# link_pattern = r'\[.*?\]\((.*?)\)' # links with labels
LINK_PAT = regex.compile(r'\((.*?)\)') # links without labels
# Regex pattern to find paragraphs containing the file link
# (?s) makes dot match newlines, enabling multi-line paragraph matching.
# para_pattern = rf'(?s)(?<=\n\n|^)(.*?\[.*?\]\({regex.escape(file_link)}\).*?)(?=\n\n|$)'


pd.set_option('display.max_rows', None)

#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from pathlib import Path
from attr import fields
import regex
from document import Document
import pandas as pd
from functools import wraps
from utility import load_config

# Regex pattern to capture markdown file links
# link_pattern = r'\[.*?\]\((.*?)\)' # links with labels
LINK_PAT = regex.compile(r'\((.*?)\)') # links without labels
# Regex pattern to find paragraphs containing the file link
# (?s) makes dot match newlines, enabling multi-line paragraph matching.
# para_pattern = rf'(?s)(?<=\n\n|^)(.*?\[.*?\]\({regex.escape(file_link)}\).*?)(?=\n\n|$)'
COMMENT_PAT = regex.compile(r'<!--(.*?)-->') 
WORDS_PAT = regex.compile(r'\b\w+\b')

pd.set_option('display.max_rows', None)

def truncate_story_path(filepath):
	root = Path.cwd().parts[-1]
	
	# Convert to Path object if not already
	p = Path(filepath) 
	parts = []
	# work backwards until we reach the root folder name
	for part in reversed(p.parts):
		if part == root:
			break
		parts.append(part) 
	
	# Reconstruct the path with the truncated parts
	return Path(*reversed(parts))


def load_index(index_file,  heading_level=2):
	index_doc = Document.read_file(index_file)
   
	# Regular expression to match only the specified heading level
	heading_pat = rf'^(?P<level>{"#" * heading_level}) (?P<heading>[^\n]+)\n'
	first_word_pat = regex.compile(r'^(\w+)\:')
	# heading_pat = rf'^(?P<level>{regex.escape("#" * heading_level)})\s+(?P<heading>[^\n]+)\n'

	# Find all headings of the specified level
	matches = list(regex.finditer(heading_pat, index_doc.content, regex.MULTILINE))
	# print(matches)

	# List to store the resulting sections
	paragraphs = []

	# Iterate over the matches and capture text between the specified heading level
	for i, match in enumerate(matches):
		# Get heading text (level is known since it's specified by the user)
		heading = match.group('heading')

		# Calculate the start of the section (just after the current heading)
		start_pos = match.end()

		# Calculate the end of the section (just before the next heading of the same level or end of the text)
		if i + 1 < len(matches):
			end_pos = matches[i + 1].start()
		else:
			end_pos = len(index_doc.content,)

		# Extract the text between this heading and the next heading of the same level
		
		content = index_doc.content[start_pos:end_pos].strip() 

		# Split text into paragraphs and flag first character
		for paragraph in content.split('\n\n'):
			if (m := first_word_pat.match(paragraph)):
				first_word = m.groups(1) 
			else:
				first_word = None

		# Add the dictionary with heading info and content to the list
			paragraphs.append({
				'heading': heading.strip(),
				'level': heading_level,
				'sequence': i,
				'paragraph': paragraph,
				'first_word': first_word
			})

	df = pd.DataFrame(paragraphs)
	df['filepaths'] = df.paragraph.apply(lambda x: [truncate_story_path(l) for l in LINK_PAT.findall(x)])
	return df.explode('filepaths').rename(columns={'filepaths': 'filepath'}).dropna(subset='filepath') 

def load_docs(doc_dir):
	df =  pd.DataFrame([Document.read_file(fp).asdict() for fp in doc_dir.rglob('*.md')]) 
	df['filepath'] = df.filepath.apply(lambda x: truncate_story_path(x))   
	df_metadata = df['metadata'].apply(pd.Series)
	return pd.concat([df.drop(columns=['metadata']), df_metadata], axis=1).set_index('identifier')
	

def display(df, **labels):
	if len(df) > 0:
		print(df.rename(mapper=labels, axis=1)[labels.values()].to_string(index=False))
	else:
		print('No Items Found')  


@define
class ContentAnalyse():
	dfd = field()
	dfi = field()
	base_dir = field(converter=Path)
	index_file = field(default='content_index.md')
	story_dir= field(default='stories', converter=Path)
	edit_path = field(default='edits', converter=Path) 
	
	@classmethod 
	def load_config_data(cls):
		field_names = [f.name for f in fields(ContentAnalyse)]
		config_values = load_config()
		config_values['dfd'] = load_docs(Path(config_values.get('story_dir', 'stories')))
		config_values['dfi'] = load_index(config_values.get('index_file', 'content_index.md'))
		return cls(**{k:v for k,v in config_values.items() if k in field_names})
	
	def content_summary(self, group=False):
		self.dfd['words'] = self.dfd.content.apply(lambda x: len(WORDS_PAT.findall(x)))
		dfc = self.dfi.merge(self.dfd, on='filepath')
		dfc['section'] = dfc.apply(lambda x: f'{x.sequence +1}: {x.heading}', axis=1)
		dfs = dfc.sort_values(by='sequence')
		if group:
			print(dfs.groupby(['section'], sort=False).agg({'status': set, 'words':'sum'}))
		else:
			display(dfs, **dict(section='Section', title='Title', status='Status', words='Words'))
		

	def comments(self):
		self.dfd['comments'] = self.dfd.content.apply(lambda x: COMMENT_PAT.findall(x, regex.DOTALL))
		df = self.dfd[self.dfd.comments.str.len() > 0].explode('comments')
		for row in df.itertuples():
			print(row.filepath)
			print(row.comments.strip())
			print('=' * 30)
	
	
	def total_words(self):
		dfw = self.dfi.merge(self.dfd, on='filepath')
		dfw['words'] = dfw.content.apply(lambda x: len(WORDS_PAT.findall(x)))
		total_words = dfw.words.sum()  # Sum all values in the specified column
		print(f"The total number of words is: {total_words}")

	def unplaced_stories(self):
		dfdi = self.dfd.merge(self.dfi, on='filepath', how='outer')
		if not (dfm := dfdi[dfdi.heading.isna()]).empty:
			print(dfm[['filepath']].to_string(index=False)) 

	def missing_stories(self):
		dfdi = self.dfd.merge(self.dfi, on='filepath', how='outer')
		if not (dfm := dfdi[dfdi.title.isna()]).empty:
			print(dfm[['heading', 'filepath']].to_string(index=False)) 

	def duplicated_links(self):
		dfdi = self.dfd.merge(self.dfi, on='filepath', how='outer')
		if not (dups := dfdi[dfdi.filepath.duplicated(keep=False)]).empty:
			print(dups[['heading', 'filepath']].to_string(index=False)) 



if __name__ == "__main__":
	fire.Fire(ContentAnalyse.load_config_data())