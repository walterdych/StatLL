import pandas as pd
import ast
import random
import numpy as np
from pydub import AudioSegment
import os
import argparse

seq_num = 1 # 1, 2, or 3
combo_num = 6 # 5, 6, or 7


# Function to create a stimulus
def create_stimulus(pattern, syllables, condition):
    stimulus = AudioSegment.empty()  # Create an empty audio segment

    # Repeat the pattern twice
    pattern = pattern * 2

    for i in range(len(pattern)):
        # Select the syllable
        syllable = syllables[i]

        # Add the suffix
        if pattern[i] != 1:
            syllable += '_' + str(pattern[i])

        # Combine the syllable files
        syllable_file = AudioSegment.from_file(os.path.join('C:/Users/cosmo/OneDrive/Desktop/Tools/SL_sequence_weighting/stim/','f1_' + syllable + '.wav'), format='wav')

        # Append the syllable to the stimulus
        stimulus += syllable_file

    # Export the stimulus
    stimulus.export(f"{condition}_{seq_num}_lengthened_stimulus.wav", format='wav')

    # Play the stimulus 4 times
    stimulus = stimulus * 4
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

    # Pick a simple pattern and a complex pattern at random
    simple_pattern = random.choice(simple_patterns)
    complex_pattern = random.choice(complex_patterns)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate lengthened stimulus.")
    parser.add_argument("seq_num", type=int, help="Sequence number for the stimulus")
    parser.add_argument("combo_num", type=int, help="Combo number for the stimulus")
    parser.add_argument("condition", type=str, help="Condition for the stimulus (e.g., 'simple', 'complex')")
    args = parser.parse_args()

    main(args.seq_num, args.combo_num, args.condition)