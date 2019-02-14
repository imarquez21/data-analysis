import pandas as pd
import argparse
import datetime


def load_model(pickle_file, old_model):

    model = pd.read_pickle(pickle_file)
    old_model = pd.read_pickle(old_model)

    print "Pause"

    return 0

def main():

    print "Script start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True, help="Pickle file associated to the model.")
    parser.add_argument('-o', '--old', type=str, required=True, help="Previous pickle file associated to the model.")

    args = vars(parser.parse_args())

    load_model(args["file"], args["old"])

    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()