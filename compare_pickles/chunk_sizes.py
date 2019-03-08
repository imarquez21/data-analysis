import pandas as pd
import argparse
import datetime
import pyprind
import os
import numpy as np

def compute_chunkSizes(chunks):

    chunkSizes = []
    size = 0
    for index, row in chunks.iterrows():

        if row["DonwBytes"] == 152:
            continue
        elif row["TsStart"] == 0:
            chunkSizes[-1] += row["DonwBytes"]
        else:
            chunkSizes.append(row["DonwBytes"])

    print np.sum(chunkSizes)

    print "Pause"



    return 0

def load_pickles(chunks_pickle):

    print "Loading Pickle."

    chunks = pd.read_pickle(chunks_pickle)

    compute_chunkSizes(chunks)

    return 0

def main():

    print "Script start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--pickle', type=str, required=True, help="Pickle file with chunks to be fixed.")

    args = vars(parser.parse_args())

    load_pickles(args["pickle"])
    # load_pickles(args["gt"], args["deployment"])

    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()