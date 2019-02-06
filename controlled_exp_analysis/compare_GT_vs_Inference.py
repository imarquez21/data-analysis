import pandas as pd
import os
import datetime
import argparse


def get_startup_differences(gt_values, inferred_values):

    print "Computing difference for startup."

    startup_differences = []

    for i in range(len(gt_values)):
        startup_differences.append(inferred_values[i] - gt_values)

    return startup_differences

def get_resolution_differences(gt_values, inferred_values):

    print "Computing difference for resolution."

    res_values = gt_values.unique()

    res_differences = []

    cont = 0
    for prediction in inferred_values:
        res_differences.append(res_values.index(prediction) - res_values.index(inferred_values[cont]))
        cont += 1

    return res_differences

def get_values_to_compare(gt_inference_df, target):

    print "Obtaining values to compare."

    if target == "s":
        gt_values = gt_inference_df["startup_mc"]
        inferred_values = gt_inference_df["startup_time"]
        get_startup_differences(gt_values, inferred_values)
    else:
        gt_values = gt_inference_df["resolution_mc"]
        inferred_values = gt_inference_df["resolution"]
        get_resolution_differences(gt_values, inferred_values)


    return 0

def load_pickle(gt_with_inf_pickle):

    print "Loading Pickle"

    gt_and_inf_df = pd.read_pickle(gt_with_inf_pickle)

    return gt_and_inf_df

def main():

    print "Script Start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", type=str, required=True, help="Inference Pickle file which contains the columns for predicted and GT metric.")
    parser.add_argument("-t", "--target", type=str, required=True, help="Metric to review, i.e. 's' [startup] or 'r' [resolution]")
    # parser.add_argument("-o", "--outdir", type=str, required=True, help="Directory where results are to be saved.")

    args = vars(parser.parse_args())

    gt_with_inf_pickle = args["file"]
    target = args["target"]
    # out_dir = args["outdir"]

    gt_inference_df = load_pickle(gt_with_inf_pickle)
    get_values_to_compare(gt_inference_df, target)


    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()