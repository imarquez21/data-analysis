import pandas as pd
import argparse
import datetime
import os


def save_pickle(all_res_no_first_min, out_dir):

    print "Saving all resolutions inference pickle after removing 1st minute per video session."

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    pickle_file = "all_res_no_first_min.pickle"

    all_res_no_first_min.to_pickle(out_dir + "/" +pickle_file)

    return 0

def remove_first_minute(all_res_pickle):

    print "Removing first minute for all video sessions."

    all_res_no_first_min = pd.DataFrame()

    all_res_no_first_min = all_res_pickle.query("relative_timestamp > 60")

    return all_res_no_first_min

def main():
    print "Script Start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True, help="Pickle File with all resolution for all deployments.")
    parser.add_argument('-o', '--outdir', type=str, required=True, help="Directory where processed pickle will be saved.")

    args = vars(parser.parse_args())

    pickle = args["file"]
    outdir = args["outdir"]

    all_res_pickle = pd.read_pickle(pickle)

    all_res_no_first_min = remove_first_minute(all_res_pickle)

    save_pickle(all_res_no_first_min, outdir)


    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()