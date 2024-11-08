#!/home/jeremy/Python3.10Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2023 Jeremy Allan <jeremy@jeremyallan.com>

from pydub import AudioSegment
from pydub.silence import split_on_silence
from math import ceil
from pathlib import Path
from utility import staging_dir
import fire

def chunk_audio(media_filepath, max_chunk_length=1000000):
    mfp = Path(media_filepath)
    output_dir = staging_dir(prefix=mfp.stem)
    audio = AudioSegment.from_file(media_filepath)
    audio_length = len(audio)
    chunk_length = ceil(audio_length / ceil(audio_length/max_chunk_length))
    for audio_chunk in audio[::chunk_length]:
        chunk_filepath = staging_file(prefix='audio', suffix='.mp3')
        audio_chunk.export(chunk_filepath, format='mp3')
        print(chunk_filepath)


def chunk_on_silence(media_filepath, min_silence_len=1000, silence_thresh=-40):
    """
    Split an audio file on silence where segments are at least five minutes long.

    Args:
        file_path (str): Path to the audio file.
        min_silence_len (int): Minimum length of silence to detect (in ms).
        silence_thresh (int): Silence threshold (in dBFS).
        min_segment_len (int): Minimum length of each segment (in ms).

    Returns:
        list of AudioSegment: List of audio segments.
    """
   
    
    # # Load the audio file
    audio = AudioSegment.from_file(media_filepath)

    min_segment_len=1400000

    chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    
    # Merge segments to ensure minimum length
    audio_chunks = []
    current_chunk = AudioSegment.empty()

    for chunk in chunks:
        if len(current_chunk) + len(chunk) >= min_segment_len:
            audio_chunks.append(current_chunk + chunk)
            current_chunk = AudioSegment.empty()
        else:
            current_chunk += chunk

    if len(current_chunk) > 0:
        audio_chunks.append(current_chunk) 

    for audio_chunk in audio_chunks:
        chunk_filepath = staging_file(suffix='.mp3')
        audio_chunk.export(chunk_filepath, format='mp3')
        yield chunk_filepath

if __name__ == '__main__':
    print('running chunking')
    fire.Fire(chunk_audio)
       
    