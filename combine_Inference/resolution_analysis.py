import pandas as pd
import argparse
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns


def plot_CDF(service, service_resolutions):

    print "Plotting CDF for " + service + " service(s)."

    figs_path = "./Figures/resolution/"
    fig_name = service + ".png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    sorted = np.sort(service_resolutions)
    yvals = np.arange(len(sorted)) / float(len(sorted) - 1)

    plt.grid()
    plt.title("Resolution CDF [" + service.title() + "] Service(s)")
    plt.xlabel("Resolution[p]")
    plt.ylabel("p(x)")
    plt.xticks((240, 480, 360, 720, 1080), ("240", "480", "360", "720", "1080"))
    # plt.plot(sorted, yvals)
    service_resolutions.hist(cumulative=True, density=1, bins=1000)
    plt.savefig(figs_path + fig_name, dpi=900)
    # plt.show()
    plt.close()

    return 0

def get_resolutions(all_res_df):

    print "Getting all startup values."

    resolutions = all_res_df["resolution_mc"]

    plot_CDF("all", resolutions)

    services = ["amazon", "netflix", "twitch", "youtube"]

    for service in services:
        print "Getting " + service + " resolution values."

        tmp_df = all_res_df[all_res_df['session_id'].str.contains(service)]
        service_resolutions = tmp_df["resolution_mc"]

        plot_CDF(service, service_resolutions)

    return 0

def main():

    print "Script Start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', type=str, required=True, help="Pickle File with all resolutions (without 1st min) for all deployments.")

    args = vars(parser.parse_args())

    resolutions_pickle = args["file"]

    all_res_df = pd.read_pickle(resolutions_pickle)

    get_resolutions(all_res_df)

    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()

