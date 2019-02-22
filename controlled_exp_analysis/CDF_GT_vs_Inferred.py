import pandas as pd
import datetime
import argparse




def load_pickles(inf_pickle, gt_pickle):

    df_inferred = pd.read_pickle(inf_pickle)
    df_gt = pd.read_pickle(gt_pickle)

    return df_inferred, df_gt


def main():
    print "Script Start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--inferred', type=str, required=True, help="Pickle file with inferred values.")
    parser.add_argument('-g', '--gt', type=str, required=True, help="Pickle file with ground truth GT values.")
    parser.add_argument('-t', '--target', type=str, required=True, help="Target metric, resolution [r] or startup [s]")


    args = vars(parser.parse_args())

    inf_pickle = args["inferred"]
    gt_pickle = args["gt"]
    target = args["target"]

    inf_df, gt_df = load_pickles(inf_pickle, gt_pickle)

    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()