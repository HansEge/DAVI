import pandas as pd
import os
import glob


def combine_csv(path):
    extension = 'csv'
    os.chdir(path)

    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

    return combined_csv