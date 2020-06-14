list_indexed_files.py part4_edits --part $1 \
| sort_on_seq.py \
| list_file_links.py title \
| less
