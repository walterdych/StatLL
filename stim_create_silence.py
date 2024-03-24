import pandas as pd
import ast
import random
import numpy as np
from pydub import AudioSegment
import os
import argparse

def create_stimulus(pattern, silence, syllables, condition, seq_num):
    silence_duration_unit = 250  # in milliseconds
    stimulus = AudioSegment.empty()  # Create an empty audio segment
    pattern = pattern * 2
    silence = silence * 2

    for i in range(len(pattern)):
        syllable = syllables[i]
        syllable_file = AudioSegment.from_file(os.path.join('stim/', f'f1_{syllable}.wav'), format='wav')
        stimulus += syllable_file
        if i < len(silence):
            silence_duration = silence[i] * silence_duration_unit
            silence_segment = AudioSegment.silent(duration=silence_duration)
            stimulus += silence_segment

    stimulus.export(f"{condition}_{seq_num}_silence_stimulus.wav", format='wav')
    stimulus = stimulus * 4  # Repeat the stimulus 4 times
    return stimulus

def main(seq_num, combo_num, condition):
    if seq_num == 1:
        syllable_list = ['tu', 'pi', 'ro', 'go', 'la', 'bu', 'bi', 'da', 'ku', 'pa', 'di', 'ta']
        wordlist = ['tupiro', 'golabu', 'bidaku', 'padita']
        target_syll = 'bu'
        target_syll_idx = 5  # Adjusted for 0-based indexing

    elif seq_num == 2:
        syllable_list = ['ra', 'ge', 'do', 'fi', 'lo', 'za', 'yu', 'ma', 'le', 'bo', 'ka', 'mi']
        wordlist = ['ragedo', 'filoza', 'yumale', 'bokami']
        target_syll = 'do'
        target_syll_idx = 2  # Adjusted for 0-based indexing

        # Adjusted for 0-based indexing. Python ranges exclude the last number, so no need to subtract 1 at the end
        word_item_syllList = [list(range(3, 6)), list(range(6, 9))]
        partword_item_syllList = [[11, 0, 1], [2, 9, 10]]

    elif seq_num == 3:
        syllable_list = ['pu', 'wa', 'lo', 'ti', 'zu', 'ye', 'be', 'mo', 'ra', 'to', 'he', 'du']
        wordlist = ['puwalo', 'tizuye', 'bemora', 'tohedu']
        target_syll = 'du'
        target_syll_idx = 11  # Adjusted for 0-based indexing

        word_item_syllList = [list(range(0, 3)), list(range(6, 9))]
        partword_item_syllList = [[11, 3, 4], [5, 9, 10]]

    # Read the CSV file
    df = pd.read_csv(f'stim_conditions/combo_chart_{combo_num}.csv')
    # Extract the patterns, convert them to lists, and convert the elements of the lists to integers
    simple_patterns = [[int(x) for x in ast.literal_eval(pattern)] for pattern in df['simple'].dropna().tolist()]
    complex_patterns = [[int(x) for x in ast.literal_eval(pattern)] for pattern in df['complex'].dropna().tolist()]
    simple_silence_patterns = [[int(x) for x in ast.literal_eval(pattern)] for pattern in df['simple_silence'].dropna().tolist()]
    complex_silence_patterns = [[int(x) for x in ast.literal_eval(pattern)] for pattern in df['complex_silence'].dropna().tolist()]

    # Pick a simple pattern
    simple_pattern = random.choice(simple_patterns)
    # Get corresponding silence pattern stored in adjacent column
    simple_silence_pattern = df['simple_silence'][simple_patterns.index(simple_pattern)]

    # Pick a complex pattern
    complex_pattern = random.choice(complex_patterns)
    # Get corresponding silence pattern stored in adjacent column
    complex_silence_pattern = df['complex_silence'][complex_patterns.index(complex_pattern)]
    # Extract the silence patterns, convert them to lists, and convert the elements of the lists to integers
    simple_silence_pattern = [int(x) for x in ast.literal_eval(df['simple_silence'].dropna().tolist()[0])]
    complex_silence_pattern = [int(x) for x in ast.literal_eval(df['complex_silence'].dropna().tolist()[0])]

    # Define the duration of a silence value of 1
    silence_duration_unit = 250  # in milliseconds


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate stimulus with silence.")
    parser.add_argument("seq_num", type=int, help="Sequence number for the stimulus")
    parser.add_argument("combo_num", type=int, help="Combo number for the stimulus")
    parser.add_argument("condition", type=str, help="Condition for the stimulus (e.g., 'control', 'experimental')")
    args = parser.parse_args()

    main(args.seq_num, args.combo_num, args.condition)


