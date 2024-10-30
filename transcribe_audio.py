#!/home/jeremy/Python3.12Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com>

from pathlib import Path
import redis
import json
import pypandoc
from uuid import uuid4
from datetime import timedelta
from oai import chat, transcribe, chunk_audio, OutputDoc
from utility import staging_file, random_string
import fire


rd = redis.Redis(decode_responses=True)

def get_dict_value(rkey, hkey):
    if rd.hexists(rkey, hkey):
        return rd.hget(rkey, hkey)
    else:
        raise KeyError(f'{hkey} does not exist')
    
class Transcriber():
    def __init__(self, job_id):
        self.job_id = job_id 
        self.index_key = f'{job_id}:processes'

    def prepare_source_audio(self, source_filename, chunk_length=5):
        source_filepath = self.source_path.joinpath(source_filename)
        edit_path = self.edit_path.joinpath(self.job_id)
        print(f'Parsing {source_filepath}')
        for i, segment in enumerate(chunk_audio(source_filepath, chunk_length)):
            print(f'Creating chunk {i}')
            chunk_filepath = staging_file(prefix=self.job_id, suffix='.mp3')
            segment.export(chunk_filepath, format='mp3')
            process_key = random_string(8)
            edit_filepath = self.edit_path.joinpath(f'{self.job_id}_{i:0{2}d}').with_suffix('.md')
            process_data = dict(
                chunk_filepath=str(chunk_filepath),
                edit_filepath = str(edit_filepath),
                document_metadata = json.dumps(dict(
                                        process_key=process_key,
                                        timecode=f'{i*5:0{2}}:00',
                                        source=source_filepath.stem)))
            
            rd.hset(process_key, mapping=process_data)
            rd.rpush(self.index_key, process_key)
            rd.expire(process_key, timedelta(days=1))
        rd.expire(self.index_key, timedelta(days=1))
        return self

    def transcribe_audio(self, process_key=None):
        print('Loading media data')
        overwrite = False
        if process_key:
            process_keys = [process_key] 
            overwrite = True
        else:
            process_keys = [k for k in rd.lrange(self.index_key, 0, -1) if not Path(get_dict_value(k, 'edit_filepath')).exists()]
        print(f'Processing {f'{len(process_keys)}'}')
        written_files = 0
        for pk in process_keys:
            edit_filepath = Path(get_dict_value(pk, 'edit_filepath'))
            edit_filepath.parent.mkdir(parents=True, exist_ok=True)
            op = OutputDoc(filepath=edit_filepath, 
                        metadata=json.loads(get_dict_value(pk, 'document_metadata')), 
                        overwrite=overwrite)
            try:
                rs = chat(self.format_instructions, transcribe(get_dict_value(pk, 'chunk_filepath')))
            except Exception as e:
                print(e)
            else:
                written_files += 1
                op.write_results(rs)
        return f'{written_files} keys written to {self.edit_path}/{self.job_id}'
    
    def output_transcriptions(self, filename):
        outputfile = self.output_dir.joinpath(filename)
        return pypandoc.convert_file([f for f in self.edit_dir.iterdir()], 'docx', outputfile=outputfile)

if __name__ == '__main__':
    fire.Fire(Transcriber)

