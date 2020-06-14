list_indexed_files.py edits --component main_text --section p3 \
| sort_on_seq.py \
| extract_field_values.py filepath \
| convert_to_tmp.sh output_sections \
| convert_from_tmp.sh output_project test_output2.docx
