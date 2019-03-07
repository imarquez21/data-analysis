import pandas as pd
import argparse
import datetime
import pyprind
import os


def compare_exp_df_vs_ta_df(exp_st, exp_et, exp_df, ta_df):

    print "Obtaining nearest session in TA df based on experiment start time."

    ta_df.sort_values("start_ts", inplace=True)
    ta_df.set_index("start_ts", inplace=True)

    startloc = ta_df.index.get_loc(exp_st, method="nearest")
    endloc = ta_df.index.get_loc(exp_et, method="nearest")

    ta_df_slice = ta_df[startloc:endloc]

    print "Pause"


    return 0

def get_experiment_timestamp(gt_df, exp_id):

    print "Getting experiment timestamp."

    temp_df = gt_df.query("session_id == '"+str(exp_id)+"'")

    temp_df.sort_values("start_ts", inplace=True)

    session_st = temp_df.iloc[0]["start_ts"]
    session_et = temp_df.iloc[-1]["start_ts"]

    return session_st, session_et, temp_df

def get_session_to_compare(gt_df, ta_df, exp_id):

    print "Getting slice of GT and TA dataframes to compare based on session ID."

    gt_df_slice = gt_df.query("session_id == '" + str(exp_id) + "'")
    ta_df_slice = ta_df.query("session_id == '" + str(exp_id) + "'")

    ta_slice_new = ta_df_slice.query("size > 0")

    gt_df_slice.sort_values("start_ts", inplace=True)
    ta_slice_new.sort_values("start_ts", inplace=True)

    print "Pause"


    return 0


def load_pickles(gt_pickle, inference_pickle):

    print "Loading pickles"

    gt_df = pd.read_pickle(gt_pickle)
    inference_df = pd.read_pickle(inference_pickle)

    # compare_res(gt_df, inference_df)
    return gt_df, inference_df

def main():

    print "Script start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gt', type=str, required=True, help="Pickle file associated to GT.")
    parser.add_argument('-d', '--deployment', type=str, required=True, help="Pickle file associated to inference based on deployment data.")
    parser.add_argument('-s', '--exp_id', type=str, required=True,
                        help="Experiment ID from GT to be compared against TA data.")

    args = vars(parser.parse_args())
    exp_id = args["exp_id"]

    gt_df, ta_df = load_pickles(args["gt"], args["deployment"])

    get_session_to_compare(gt_df, ta_df, exp_id)

    # exp_st, exp_et, exp_df = get_experiment_timestamp(gt_df, exp_id)
    # compare_exp_df_vs_ta_df(exp_st, exp_et, exp_df, ta_df)


    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()