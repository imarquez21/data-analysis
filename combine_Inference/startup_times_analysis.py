import pandas as pd
import argparse
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn


def plot_CDF(service, sts_times):

    print "Plotting CDF for " + service + " service(s)."

    figs_path = "./Figures/"
    fig_name = service + ".png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    sorted = np.sort(sts_times)
    p = 1. * np.arange(len(sts_times)) / (len(sts_times) - 1)

    # num_bins = 20
    # counts, bin_edges = np.histogram(sts_times, bins=num_bins, normed=True)
    # cdf = np.cumsum(counts)

    plt.grid(0)
    plt.title("Startup Time [" + service.title() + "] Service(s)")
    plt.xlabel("Time [sec]")
    plt.ylabel("p(x)")
    plt.plot(sorted, p)
    # plt.plot(bin_edges[1:], cdf / cdf[-1])
    plt.savefig(figs_path + fig_name, dpi=900)
    # plt.show()
    plt.close()

    return 0

def get_startup_times(startups_df):

    print "Getting all startup values."

    sts_times = startups_df["startup_mc"].div(1000)

    plot_CDF("all", sts_times)

    services = ["amazon", "netflix", "twitch", "youtube"]

    for service in services:
        print "Getting " + service + "startup values."

        tmp_df = startups_df[startups_df['session_id'].str.contains(service)]
        service_sts_time = tmp_df["startup_mc"].div(1000)

        plot_CDF(service, service_sts_time)

    return 0

def main():

    print "Script Start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', type=str, required=True, help="Pickle File with all startup times for all deployments.")

    args = vars(parser.parse_args())

    startups_pickle = args["file"]

    all_sts_df = pd.read_pickle(startups_pickle)

    get_startup_times(all_sts_df)

    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()

