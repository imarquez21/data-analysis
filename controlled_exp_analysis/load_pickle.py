import pandas as pd
import os
import datetime
import argparse


def main():
    print "Script Start."
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--pickle', type=str, required=True, help="Pickle file to be loaded.")

    args = vars(parser.parse_args())

    pickle_file = args["pickle"]

    df = pd.read_pickle(pickle_file)

    print "Pause"


    print "Script End."
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()