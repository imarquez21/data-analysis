import pandas as pd
import os
import datetime
import argparse
import numpy as np
import itertools as iter
import matplotlib.pyplot as plt
from scipy import stats


def plot_bars_resolution_differences(res_differences):

    print "Plotting difference between GT and Inferred Bars plot."

    fig_path = "./Figures/Differences/"
    fig_file = "res_difference_bar.png"

    if not os.path.exists(fig_path):
        os.makedirs(fig_path)

    res_differences = np.array(res_differences)

    freqs = stats.itemfreq(res_differences)

    differnces_freqs_df = pd.DataFrame(data=freqs, columns=["Difference", "Counts"])

    differnces_freqs_df.plot.bar(x="Difference", y="Counts", rot=0)

    plt.grid()
    plt.title("Resolution GT vs Inferred Class Differences")
    plt.xlabel("Num. Class Difference")
    plt.ylabel("Counts")
    plt.savefig(fig_path + fig_file, dpi=600)
    plt.close()

    return 0

def plot_differences_CDF(differences, target):

    print "Plotting difference between GT and Inferred CDF."

    fig_path = "./Figures/Differences/"

    if not os.path.exists(fig_path):
        os.makedirs(fig_path)

    sorted_data = np.sort(differences)
    yvals = np.arange(len(sorted_data)) / float(len(sorted_data) - 1)


    if target == 's':
        fig_file = "startup_differences.png"
        plt.grid()
        plt.title("Startup GT vs Inferred Differences CDF")
        plt.xlabel("Time [sec]")
        plt.ylabel("P(x)")
        plt.plot(sorted_data, yvals)
        plt.savefig(fig_path + fig_file, dpi=600)
        plt.close()

    else:
        fig_file = "resolution_differences.png"
        plt.grid()
        plt.title("Startup GT vs Inferred Differences CDF")
        plt.xlabel("Class")
        plt.ylabel("P(x)")
        plt.plot(sorted_data, yvals)
        plt.savefig(fig_path + fig_file, dpi=600)
        plt.close()


    return 0

def get_startup_differences(gt_values, inferred_values):

    print "Computing difference for startup."

    startup_differences = []

    for gt, predicted in iter.izip(gt_values, inferred_values):
        startup_differences.append(predicted - gt)

    plot_differences_CDF(startup_differences, "s")

    return startup_differences

def get_resolution_differences(gt_values, inferred_values):

    print "Computing difference for resolution."

    resolution_differences_df = pd.DataFrame(columns=["Inferred", "GT", "Difference"])
    res_values = []

    # Dynamically populate the resolution values arrays
    # to make sure the values to compare with are part of the GT and inferred sets.
    res_values.extend(gt_values.unique())
    res_values.extend(inferred_values.unique())
    res_values = np.array(res_values)
    res_values = np.sort(np.unique(res_values))

    # Fixed array, after testing this array contains all (so far) values to
    # to be found in the GT and inferred tests. Uncommment to work with a fixed array.
    # res_values = [0, 240, 288, 360, 384, 432, 480, 540, 720, 864, 1080]

    res_differences = []
    gt_vals = []
    predicted_vals = []

    for gt, predicted in iter.izip(gt_values, inferred_values):
        if gt == 0: # Skip the entries where GT was unable to get the resolution.
            continue
        else:
            index_gt, = np.where(res_values == gt)
            index_predicted, = np.where(res_values == predicted)
            gt_vals.append(gt)
            predicted_vals.append(predicted)
            res_differences.append(index_predicted[0] - index_gt[0])

    resolution_differences_df["Inferred"] = predicted_vals
    resolution_differences_df["GT"] = gt_vals
    resolution_differences_df["Difference"] = res_differences

    plot_bars_resolution_differences(res_differences)

    # plot_differences_CDF(res_differences, "r")

    return resolution_differences_df, res_values

def get_values_to_compare(gt_inference_df, target):

    print "Obtaining values to compare."

    if target == "s":
        gt_values = gt_inference_df["startup_time"].div(1000)
        inferred_values = gt_inference_df["startup_mc"].div(1000)
        get_startup_differences(gt_values, inferred_values)
    else:
        gt_values = gt_inference_df["resolution"].astype(int)
        inferred_values = gt_inference_df["resolution_mc"].astype(int)
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

    args = vars(parser.parse_args())

    gt_with_inf_pickle = args["file"]
    target = args["target"]

    gt_inference_df = load_pickle(gt_with_inf_pickle)
    get_values_to_compare(gt_inference_df, target)

    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()