import pandas as pd
import argparse
import datetime
import os


def save_pickle(final_df, out_file):
    print "Saving bundled pickle."

    final_df.to_pickle("./" + out_file)

    return 0

def merge_pickles(path):

    print "Merging pickles."

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".pkl") or file.endswith(".pickle"):
                tmp_df = pd.read_pickle(root + "/" + file)
                tmp_df = tmp_df.query("relative_timestamp > 60")
                final_df = final_df.append(tmp_df)
            else:
                continue

    return final_df


def main():
    print "Script Start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, required=True, help="Directory where pickles are stored")
    parser.add_argument('-o', '--outfile', type=str, required=True, help="Filename to be given to output pickle")

    args = vars(parser.parse_args())

    directory = args["dir"]
    out_file = args["outdir"]

    final_df = merge_pickles(directory)
    save_pickle(final_df, out_file)


    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()
