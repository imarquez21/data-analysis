import pandas as pd
import os
import datetime
import argparse


def save_pickle(features_df, out_dir, deployment):

    print "Saving " + deployment + " features pickle."

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    out_file = deployment + "_features.pickle"

    features_df.to_pickle(out_dir + "/" + out_file)

    return 0

def merge_pickles(path, deployment):

    print "Merging " + deployment + " features pickles."

    features_df = pd.DataFrame()

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".pkl") or file.endswith(".pickle"):
                tmp_df = pd.read_pickle(root + "/" + file)
                features_df = tmp_df.append(tmp_df)
            else:
                continue

    return features_df

def main():

    print "Script Start."
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dir', type=str, required=True, help="Directory where pickles are stored")
    parser.add_argument('-o', '--outdir', type=str, required=True, help="Directory where comnbined pickles will be saved")

    args = vars(parser.parse_args())

    dir = args["dir"]
    out_dir = args["outdir"]

    if dir.endswith("/"):
        deployment = dir.split("/")[-2]
    else:
        deployment = dir.split("/")[-1]
    

    features_df = merge_pickles(dir)
    save_pickle(features_df, out_dir, deployment)


    print "Script End."
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()