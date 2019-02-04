import pandas as pd
import argparse
import datetime
import os

def save_pickle(inference_df, out_dir, target):

    print "Saving " + target + " inference pickle."

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    pickle_file = "all_"+target+".pickle"

    inference_df.to_pickle(out_dir + "/" +pickle_file)

    return 0

def merge_inference_pickles(path, target):

    print "Merging "+target+" pickles."

    inference_df = pd.DataFrame()

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".pkl") or file.endswith(".pickle"):
                tmp_df = pd.read_pickle(root + "/" + file)
                inference_df = inference_df.append(tmp_df)
            else:
                continue

    return inference_df


def main():
    print "Script Start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, required=True, help="Directory where pickles are stored")
    parser.add_argument('-o', '--outdir', type=str, required=True, help="Directory where comnbined pickles will be saved")

    args = vars(parser.parse_args())

    directory = args["dir"]
    out_dir = args["outdir"]
    targets = ["startup", "resolution"]


    for target in targets:
        path = directory + "/" + target
        inference_df = merge_inference_pickles(path, target)
        save_pickle(inference_df, out_dir, target)


    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()
