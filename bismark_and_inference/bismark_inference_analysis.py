import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import csv
from datetime import datetime
import argparse
import seaborn as sns
plt.style.use('seaborn')

def plot_inference_startup_CDF(df, percentile):

    print "Plotting CDF for Inference Startup - Perc "+str(percentile)

    figs_path = './Figures/Inference_CDF/'
    fig_name = 'CDF_Startup_Perc_' + str(percentile) + '.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    column_tag = "start_"+str(percentile)+"_perc"
    data = df[column_tag].values
    values = []

    for entry in data:
        values.append(entry/1000)

    values = np.sort(values)
    p = 1. * np.arange(len(values)) / (len(values) - 1)
    plt.plot(values, p)
    plt.grid()
    plt.title("CDF Startup Perc "+str(percentile))
    plt.ylabel("P(x)")
    plt.xlabel("Startup "+str(percentile)+" Perc [sec]")

    plt.savefig(figs_path + fig_name, dpi=900)
    # plt.show()
    plt.close()

    return 0

def plot_inference_resolution_CDF(df, percentile):

    print "Plotting CDF for Inference Resolution - Perc " + str(percentile)

    figs_path = './Figures/Resolution_CDF/'
    fig_name = 'CDF_Resolution_Perc_' + str(percentile) + '.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    column_tag = "res_" + str(percentile)+"_perc"
    data = df[column_tag].values

    data = np.sort(data)
    p = 1. * np.arange(len(data)) / (len(data) - 1)
    plt.plot(data, p)
    plt.grid()
    plt.title("CDF Resolution Perc " + str(percentile))
    plt.ylabel("P(x)")
    plt.xlabel("Resoltuion " + str(percentile) + " Perc [p]")

    plt.savefig(figs_path + fig_name, dpi=900)
    # plt.show()
    plt.close()

    return 0

def plot_bismark_CDF(df, percentile):

    print "Plotting CDF for BISmark Data - Perc "+str(percentile)

    figs_path = './Figures/Bismark_CDF/'
    fig_name = 'CDF_Down_Perc_' + str(percentile) + '.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    column_tag = "Down_Perc_"+str(percentile)
    data = df[column_tag].values
    values = []

    for entry in data:
        values.append(entry/1000)

    values = np.sort(values)
    p = 1. * np.arange(len(values)) / (len(values) - 1)
    plt.plot(values, p)
    plt.grid()
    plt.title("CDF Down Capacity Perc "+str(percentile))
    plt.ylabel("P(x)")
    plt.xlabel("Down Capacity "+str(percentile)+" Perc [Mbps]")

    plt.savefig(figs_path + fig_name, dpi=900)
    # plt.show()
    plt.close()

    # plt.hist(values, normed=True, cumulative=True, label='CDF',
    #          histtype='step', alpha=0.8, color='k')

    return 0

def export_to_csv(master_df):

    print "Saving Dataframe as CSV"

    csvs_path = './CSVs/Consolidated/'
    csv_filename = 'final_dataset.csv'

    if not os.path.exists(csvs_path):
        os.makedirs(csvs_path)

    master_df.to_csv(csvs_path + csv_filename)

    return 0

def plot_scatter_plot(master_df, percentile):

    print "Plotting Scatter Plot Percentile "+str(percentile)

    figs_path = './Figures/Scatter_Plots/'
    fig_name = 'Scatter_plot_perc_'+str(percentile)+'.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    ax1 = master_df.plot.scatter(x='Down_Perc_'+str(percentile),
                                 y='res_'+str(percentile)+'_perc',
                                 c='DarkBlue')

    # Setting labels for the figure
    # plt.xlim(right=300)
    plt.title("Down Capacity vs Resolution")
    plt.ylabel("Resolution "+str(percentile)+" Perc [p]")
    plt.xlabel("Down Capacity "+str(percentile)+" Perc [Mbps]")

    plt.savefig(figs_path + fig_name, dpi=900)
    # plt.show()
    plt.close()

    return 0

def clean_master_df(master_df):

    print "Formatting Dataframe to proceed with plots."

    master_df = master_df.dropna()

    # Divide by 1000 to have Mbps
    master_df['Avg_Down'] = master_df['Avg_Down'].div(1000)
    master_df['Avg_Up'] = master_df['Avg_Up'].div(1000)
    master_df['Down_Perc_50'] = master_df['Down_Perc_50'].div(1000)
    master_df['Down_Perc_75'] = master_df['Down_Perc_75'].div(1000)
    master_df['Down_Perc_85'] = master_df['Down_Perc_85'].div(1000)
    master_df['Down_Perc_90'] = master_df['Down_Perc_90'].div(1000)
    master_df['Up_Perc_50'] = master_df['Up_Perc_50'].div(1000)
    master_df['Up_Perc_75'] = master_df['Up_Perc_75'].div(1000)
    master_df['Up_Perc_85'] = master_df['Up_Perc_85'].div(1000)
    master_df['Up_Perc_90'] = master_df['Up_Perc_90'].div(1000)

    # Divide by 1000 to go from msecs to secs
    master_df['start_avg'] = master_df['start_avg'].div(1000)
    master_df['start_50_perc'] = master_df['start_50_perc'].div(1000)
    master_df['start_75_perc'] = master_df['start_75_perc'].div(1000)
    master_df['start_85_perc'] = master_df['start_85_perc'].div(1000)
    master_df['start_90_perc'] = master_df['start_90_perc'].div(1000)

    export_to_csv(master_df)

    percentiles = [50, 75, 85, 90]

    for perc in percentiles:
        plot_scatter_plot(master_df, perc)

    return 0

def load_CSVs(path):

    print "Loading CSVs"

    percentiles = [50, 75, 85, 90]

    df_bismark = pd.DataFrame.from_csv(path+'Bitrate_per_deployment.csv')
    df_bismark = df_bismark.set_index('deployment_id')

    # for perc in percentiles:
    #     plot_bismark_CDF(df_bismark, perc)

    df_res = pd.DataFrame.from_csv(path+'resolution_stats.csv')
    df_res.columns = ["res_75_perc", "res_50_perc", "res_avg", "res_90_perc", "res_85_perc"]

    # for perc in percentiles:
    #     plot_inference_resolution_CDF(df_res, perc)

    df_startup = pd.DataFrame.from_csv(path+'startup_stats.csv')
    df_startup.columns = ["start_75_perc", "start_50_perc", "start_avg", "start_90_perc", "start_85_perc"]

    for perc in percentiles:
        plot_bismark_CDF(df_bismark, perc)
        plot_inference_resolution_CDF(df_res, perc)
        plot_inference_startup_CDF(df_startup, perc)

    # Merge inference Dataframes
    df_final = df_res.add(df_startup, fill_value=0)

    # Merge inference dataframes with BISmark dataframe
    df_master = df_bismark.add(df_final, fill_value=0)

    # Call to remove row and columns with NaN values from master dataframe
    clean_master_df(df_master)

    return 0

def plot_CDF_target(metric_df, target):

    print "Plottig CDF for "+target

    figs_path = './Figures/Inference_CDF/'
    fig_name = target+'_CDF.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    values = metric_df["metric"].values
    values = np.sort(values)
    p = 1. * np.arange(len(values)) / (len(values) - 1)
    plt.plot(values, p)
    plt.grid()
    plt.title(target.title() + " CDF")
    plt.ylabel("P(x)")
    if target == "startup":
        plt.xlabel("Startup Time [sec]")
    else:
        plt.xlabel("Resolution [p]")
        plt.xticks((240, 480, 360, 720, 1080), ("240", "480", "360", "720", "1080"))

    plt.savefig(figs_path + fig_name, dpi=900)
    # plt.show()
    plt.close()

    return 0

def mac_address_to_deployment_id(bitrate_df):

    with open("./CSVs/deployment_ID_MAC_mapping.csv", mode='r') as infile:
        reader = csv.reader(infile)
        mapping_dict = dict((rows[1], rows[0]) for rows in reader)


    mac_address_list = bitrate_df["Device_ID"].values
    deployment_ids = []

    for mac_address in mac_address_list:
        deployment_id = mapping_dict.get(mac_address, "NA")
        deployment_ids.append(deployment_id)

    bitrate_df["deployment"] = deployment_ids

    bitrate_df = bitrate_df.drop(labels=["Device_ID"], axis=1)

    bitrate_df = bitrate_df.sort_values(["deployment", "Event_date"])

    bitrate_df = bitrate_df[["deployment", "Event_date", "Avg"]]

    bitrate_df.columns = ["deployment", "Event_date", "Down_bitrate"]

    return bitrate_df

def load_merge_dfs_by_time(path, target, with_service = False):

    print "Loading and merging data frames by time."

    bitrate_df = pd.DataFrame.from_csv(path + "Down_bitrate_by_time.csv")
    bitrate_df = mac_address_to_deployment_id(bitrate_df)

    if with_service:
        metric_df = pd.DataFrame.from_csv(path + target + "_with_service_stats_by_time.csv")
        metric_df = metric_df[["deployment", "Event_date", "metric", "service", "session_ids"]]
    else:
        metric_df = pd.DataFrame.from_csv(path + target + "_stats_by_time.csv")
        metric_df = metric_df[["deployment", "Event_date", "metric"]]

    return bitrate_df, metric_df

def plot_scatter_infer_vs_down_bitrate(deployment, down_bitrate, metric, target):

    print deployment.title() +": Preparing data to plot scatter plot down bitrates vs " + target.title()

    figs_path = "./Figures/Scatter_Plots/"+target.title()+"/All_Services/"
    fig_name = deployment+".png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    try:
        plt.scatter(down_bitrate, metric, c='C0')
        plt.title(deployment + ": Down Bitrate vs " + target.title() + " [All Services]")
        if target == "startup":
            plt.ylabel("Startup time [sec]")
        else:
            # resolutions = [240, 480, 360, 720, 1080]
            plt.yticks((240, 480, 360, 720, 1080), ("240", "480", "360", "720", "1080"))
            plt.ylabel("Resolution [p]")

        plt.xlabel("Down Bitrate [Mbps]")

        plt.savefig(figs_path + fig_name, dpi=600)
        # plt.show()
        plt.close()
    except Exception as exp:
        print "Exception for "+deployment+": "+str(exp)+"\n"

    return 0

def plot_scatter_infer_vs_down_bitrate_with_service(deployment, down_bitrate, metric, target, service):

    print deployment.title() + ": Preparing " + service + " data to plot scatter plot down bitrates vs " + target.title()

    figs_path = "./Figures/Scatter_Plots/"+target.title()+"/"+service.title()+"/"
    fig_name = deployment+".png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    try:
        plt.scatter(down_bitrate, metric, c='C0')
        plt.title(deployment + ": Down Bitrate vs " + target.title() + " [" + service + "]")
        if target == "startup":
            plt.ylabel("Startup time [sec]")
        else:
            # resolutions = [240, 480, 360, 720, 1080]
            plt.yticks((240, 480, 360, 720, 1080), ("240", "480", "360", "720", "1080"))
            plt.ylabel("Resolution [p]")

        plt.xlabel("Down Bitrate [Mbps]")

        plt.savefig(figs_path + fig_name, dpi=600)
        # plt.show()
        plt.close()
    except Exception as exp:
        print "Exception for "+deployment+": "+str(exp)

    return 0

# def create_heatmap_per_service_down_bitrate(service_metrics, service_bitrates, service, target):
#
#     print "Plotting heatmap for "+target+" for "+service
#
#     heatmap, xedges, yedges = np.histogram2d(service_metrics, service_bitrates, bins=(1024, 768))
#     extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#
#     plt.clf()
#     plt.imshow(heatmap.T, extent=extent, origin='lower')
#     plt.show()
#
#     return 0

def create_density_plots(service_metrics, service_bitrates, service, target, metric):

    if metric == "capacity":
        print "Plotting Scatter Plot, Hexbin and Heatmap for " + service + " data, inferred down capacity vs " + target
    else:
        print "Plotting Scatter Plot, Hexbin and Heatmap for " + service + " data, down throughput vs " + target

    figs_path = "./Figures/Heatmap_Plots/" + metric.title() + "/"+target.title()+"/"
    fig_name = service + ".png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    # Create a figure with 3 plot areas
    fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(21, 5))

    for i in range(3):

        if metric == "capacity":
            axes[i].set_xlabel("Down Inferred Capacity [Mbps]")
            fig.suptitle("Down Inferred Capacity vs " + target.title() + " [" + service.title() + "]")
        else:
            axes[i].set_xlabel("Down Throughput [Mbps]")
            fig.suptitle("Down Throughput vs " + target.title() + " [" + service.title() + "]")

        if target == "startup":
            axes[i].set_ylabel("Startup Time [sec]")
        else:
            axes[i].set_ylabel("Resolution [p]")
            # axes[i].set_yticks((240, 480, 360, 720, 1080), ("240", "480", "360", "720", "1080"))
            axes[i].set_yticks((240, 480, 360, 720, 1080))
            axes[i].set_yticklabels(("240", "480", "360", "720", "1080"))

    # Everything starts with a Scatterplot
    axes[0].set_title('Scatterplot')
    axes[0].plot(service_bitrates, service_metrics, 'ko')
    # As you can see there is a lot of overplottin here!

    nbins = 30

    # Thus we can cut the plotting window in several hexbins
    axes[1].set_title('Hexbin')
    # axes[1].hexbin(service_metrics, service_bitrates, gridsize=nbins, cmap=plt.cm.BuGn_r)
    axes[1].hexbin(service_bitrates, service_metrics, gridsize=nbins, cmap=plt.cm.coolwarm)

    # 2D Histogram
    axes[2].set_title('Heatmap')
    # axes[2].hist2d(service_metrics, service_bitrates, bins=nbins, cmap=plt.cm.BuGn_r)
    axes[2].hist2d(service_bitrates, service_metrics, bins=nbins, cmap=plt.cm.coolwarm)

    fig.savefig(figs_path + fig_name, dpi=600)
    # plt.show()
    plt.close()

    return 0

def plot_sns_density(service_metrics, service_bitrates, service, target, metric):

    if metric == "capacity":
        print "Plotting density plot for " + service + " data, inferred down capacity vs " + target
    else:
        print "Plotting density plot for " + service + " data, down throughput vs " + target

    figs_path = "./Figures/Density_Plots/" + metric.title() + "/"+target.title()+"/"
    fig_name = service + ".png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    sns.kdeplot(service_bitrates, service_metrics, cmap="Reds", shade=True)

    if metric == "capacity":
        plt.title("Density plot for Inferred Down Capacity vs " + target.title() + " [" + service + "]", loc='center')
        plt.xlabel("Inferred Down Capacity [Mbps]")
    else:
        plt.title("Density plot for Down Throughput vs " + target.title() + " [" + service + "]", loc='center')
        plt.xlabel("Down Throughput [Mbps]")


    if target == "startup":
        plt.ylabel("Startup time [sec]")
    else:
        # resolutions = [240, 480, 360, 720, 1080]
        plt.yticks((240, 480, 360, 720, 1080), ("240", "480", "360", "720", "1080"))
        plt.ylabel("Resolution [p]")



    plt.savefig(figs_path + fig_name, dpi=600)
    # plt.show()
    plt.close()

    return 0

def create_scatter_plot_per_service(service_metrics, service_bitrates, service, target, metric):

    if metric == "capacity":
        print "Plotting Scatter Plot for " + service + " data, inferred down capacity vs " + target
    else:
        print "Plotting Scatter Plot for " + service + " data, down throughput vs " + target

    figs_path = "./Figures/Scatter_Plots/" + metric.title() + "/"+target.title()+"/"
    fig_name = service + ".png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    try:
        plt.scatter(service_bitrates, service_metrics, c='C0')

        if metric == "capacity":
            plt.title("Down Inferred Capacity vs " + target.title() + " [" + service + "]")
            plt.xlabel("Down Inferred Capacity [Mbps]")
        else:
            plt.title("Down Throughput vs " + target.title() + " [" + service + "]")
            plt.xlabel("Down Throughput [Mbps]")

        if target == "startup":
            plt.ylabel("Startup time [sec]")
        else:
            plt.yticks((240, 480, 360, 720, 1080), ("240", "480", "360", "720", "1080"))
            plt.ylabel("Resolution [p]")

        plt.savefig(figs_path + fig_name, dpi=600)
        # plt.show()
        plt.close()
    except Exception as exp:
        print "Exception for " + service + ": " + str(exp)


    return 0

def create_scatter_plot_per_service_inf_capacity(service_metrics, service_bitrates, service, target):

    print "Preparing " + service + " data to plot scatter plot down capacity vs " + target

    figs_path = "./Figures/Scatter_Plots/" + target.title() + "/Per_Service/Capacity/"
    fig_name = service + ".png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    try:
        plt.scatter(service_bitrates, service_metrics, c='C0')
        plt.title("Down Capacity vs " + target.title() + " [" + service + "]")
        if target == "startup":
            plt.ylabel("Startup time [sec]")
        else:
            # resolutions = [240, 480, 360, 720, 1080]
            plt.yticks((240, 480, 360, 720, 1080), ("240", "480", "360", "720", "1080"))
            plt.ylabel("Resolution [p]")

        plt.xlabel("Down Capacity [Mbps]")

        plt.savefig(figs_path + fig_name, dpi=600)
        # plt.show()
        plt.close()
    except Exception as exp:
        print "Exception for " + service + ": " + str(exp)


    return 0

def prepare_data_to_plot_with_service(bitrate_df, inference_df, target, bis_metric):

    bitrate_df.set_index(pd.DatetimeIndex(bitrate_df["Event_date"]), inplace=True)
    inference_df.set_index(pd.DatetimeIndex(inference_df["Event_date"]), inplace=True)

    bitrate_deployments = bitrate_df["deployment"].unique()
    inference_deployments = inference_df["deployment"].unique()

    inference_services = inference_df["service"].unique()

    matching_deployments = set(bitrate_deployments) & set(inference_deployments)

    matching_deployments = sorted(matching_deployments)

    youtube_metrics = []
    youtube_bitrates = []
    amazon_metrics = []
    amazon_bitrates = []
    twitch_metrics = []
    twitch_bitrates = []
    netflix_metrics = []
    netflix_bitrates = []

    for deployment in matching_deployments:
        for service in inference_services:
            down_bitrate = []
            metric = []
            sub_inference_df = inference_df.loc[(inference_df["deployment"] == deployment) & (inference_df["service"] == service)]
            sub_bitrate_df = bitrate_df.loc[bitrate_df["deployment"] == deployment]

            try:
                start_date = sub_inference_df.index[0]
                end_date = sub_inference_df.index[-1]

                startloc = sub_bitrate_df.index.get_loc(start_date, method="nearest")
                endloc = sub_bitrate_df.index.get_loc(end_date, method="nearest")

                if startloc == endloc:
                    if endloc == 0:
                        sli = sub_bitrate_df[endloc:endloc + len(sub_inference_df["deployment"])]
                        down_bitrate = sli["Down_bitrate"]
                    else:
                        sli = sub_bitrate_df[endloc - (len(sub_inference_df["deployment"])):endloc]
                        down_bitrate = sli["Down_bitrate"]
                elif (endloc - startloc) > len(sub_inference_df["deployment"]):
                    for entry in sub_inference_df.index.values:
                        loc = sub_bitrate_df.index.get_loc(entry, method="nearest")
                        temp_value = sub_bitrate_df["Down_bitrate"].iloc[loc]
                        down_bitrate.append(temp_value)
                elif (endloc - startloc) < len(sub_inference_df["deployment"]):
                    sli = sub_bitrate_df[startloc:endloc]
                    down_bitrate = sli["Down_bitrate"]
                    if len(down_bitrate) < len(sub_inference_df["deployment"]):
                        sli = sub_bitrate_df[startloc:startloc + len(sub_inference_df["deployment"])]
                        down_bitrate = sli["Down_bitrate"]
                        if len(down_bitrate) < len(sub_inference_df["deployment"]):
                            sli = sub_bitrate_df[0:0 + len(sub_inference_df["deployment"])]
                            down_bitrate = sli["Down_bitrate"]

                metric = sub_inference_df["metric"].values

                if target == "resolution":
                    metric_list = []
                    for value in metric:
                        metric_list.append(value)
                    metric = metric_list

                # Make the down bitrates and inference arrays match.
                if len(down_bitrate) != len(metric):
                    if len(down_bitrate) > len(metric):
                        down_bitrate = down_bitrate[:len(metric)]
                    else:
                        metric = metric[:len(down_bitrate)]

                # plot_scatter_infer_vs_down_bitrate_with_service(deployment, down_bitrate, metric, target, service)

                if service == "youtube":
                    youtube_metrics.extend(metric)
                    youtube_bitrates.extend(down_bitrate)
                elif service == "amazon":
                    amazon_metrics.extend(metric)
                    amazon_bitrates.extend(down_bitrate)
                elif service == "twitch":
                    twitch_metrics.extend(metric)
                    twitch_bitrates.extend(down_bitrate)
                elif service == "netflix":
                    netflix_metrics.extend(metric)
                    netflix_bitrates.extend(down_bitrate)

            except Exception as excp:
                print "Exception for " + deployment + " and " + service + ": " + str(excp)

    create_scatter_plot_per_service(amazon_metrics, amazon_bitrates, "amazon", target, bis_metric)
    create_scatter_plot_per_service(twitch_metrics, twitch_bitrates, "twitch", target, bis_metric)
    create_scatter_plot_per_service(netflix_metrics, netflix_bitrates, "netflix", target, bis_metric)
    create_scatter_plot_per_service(youtube_metrics, youtube_bitrates, "youtube", target, bis_metric)

    create_density_plots(amazon_metrics, amazon_bitrates, "amazon", target, bis_metric)
    create_density_plots(twitch_metrics, twitch_bitrates, "twitch", target, bis_metric)
    create_density_plots(netflix_metrics, netflix_bitrates, "netflix", target, bis_metric)
    create_density_plots(youtube_metrics, youtube_bitrates, "youtube", target, bis_metric)

    plot_sns_density(amazon_metrics, amazon_bitrates, "amazon", target, bis_metric)
    plot_sns_density(twitch_metrics, twitch_bitrates, "twitch", target, bis_metric)
    plot_sns_density(netflix_metrics, netflix_bitrates, "netflix", target, bis_metric)
    plot_sns_density(youtube_metrics, youtube_bitrates, "youtube", target, bis_metric)

    return 0

def prepare_data_to_plot_with_service_inf_capacity(bitrate_df, inference_df, target):

    print "Perparing data to plot "+target+" with inferred capacity."

    bitrate_df.set_index(pd.DatetimeIndex(bitrate_df["Event_date"]), inplace=True)
    inference_df.set_index(pd.DatetimeIndex(inference_df["Event_date"]), inplace=True)

    bitrate_deployments = bitrate_df["deployment"].unique()
    inference_deployments = inference_df["deployment"].unique()

    inference_services = inference_df["service"].unique()

    matching_deployments = set(bitrate_deployments) & set(inference_deployments)

    matching_deployments = sorted(matching_deployments)

    youtube_metrics = []
    youtube_bitrates = []
    amazon_metrics = []
    amazon_bitrates = []
    twitch_metrics = []
    twitch_bitrates = []
    netflix_metrics = []
    netflix_bitrates = []

    for deployment in matching_deployments:
        for service in inference_services:
            down_capacity = []
            metric = []
            sub_inference_df = inference_df.loc[
                (inference_df["deployment"] == deployment) & (inference_df["service"] == service)]
            sub_bitrate_df = bitrate_df.loc[bitrate_df["deployment"] == deployment]

            try:
                start_date = sub_inference_df.index[0]
                end_date = sub_inference_df.index[-1]

                startloc = sub_bitrate_df.index.get_loc(start_date, method="nearest")
                endloc = sub_bitrate_df.index.get_loc(end_date, method="nearest")

                if startloc == endloc:
                    if endloc == 0:
                        sli = sub_bitrate_df[endloc:endloc + len(sub_inference_df["deployment"])]
                        down_capacity = sli["inf_capacity"]
                    else:
                        sli = sub_bitrate_df[endloc - (len(sub_inference_df["deployment"])):endloc]
                        down_capacity = sli["inf_capacity"]
                elif (endloc - startloc) > len(sub_inference_df["deployment"]):
                    for entry in sub_inference_df.index.values:
                        loc = sub_bitrate_df.index.get_loc(entry, method="nearest")
                        temp_value = sub_bitrate_df["inf_capacity"].iloc[loc]
                        down_capacity.append(temp_value)
                elif (endloc - startloc) < len(sub_inference_df["deployment"]):
                    sli = sub_bitrate_df[startloc:endloc]
                    down_capacity = sli["inf_capacity"]
                    if len(down_capacity) < len(sub_inference_df["deployment"]):
                        sli = sub_bitrate_df[startloc:startloc + len(sub_inference_df["deployment"])]
                        down_capacity = sli["inf_capacity"]
                        if len(down_capacity) < len(sub_inference_df["deployment"]):
                            sli = sub_bitrate_df[0:0 + len(sub_inference_df["deployment"])]
                            down_capacity = sli["inf_capacity"]

                metric = sub_inference_df["metric"].values

                if target == "resolution":
                    metric_list = []
                    for value in metric:
                        metric_list.append(value)
                    metric = metric_list

                # Make the down bitrates and inference arrays match.
                if len(down_capacity) != len(metric):
                    if len(down_capacity) > len(metric):
                        down_capacity = down_capacity[:len(metric)]
                    else:
                        metric = metric[:len(down_capacity)]

                # plot_scatter_infer_vs_down_capacity_with_service(deployment, down_capacity, metric, target, service)

                if service == "youtube":
                    youtube_metrics.extend(metric)
                    youtube_bitrates.extend(down_capacity)
                elif service == "amazon":
                    amazon_metrics.extend(metric)
                    amazon_bitrates.extend(down_capacity)
                elif service == "twitch":
                    twitch_metrics.extend(metric)
                    twitch_bitrates.extend(down_capacity)
                elif service == "netflix":
                    netflix_metrics.extend(metric)
                    netflix_bitrates.extend(down_capacity)

            except Exception as excp:
                print "Exception for " + deployment + " and " + service + ": " + str(excp)

    create_scatter_plot_per_service_inf_capacity(amazon_metrics, amazon_bitrates, "amazon", target)
    create_scatter_plot_per_service_inf_capacity(twitch_metrics, twitch_bitrates, "twitch", target)
    create_scatter_plot_per_service_inf_capacity(netflix_metrics, netflix_bitrates, "netflix", target)
    create_scatter_plot_per_service_inf_capacity(youtube_metrics, youtube_bitrates, "youtube", target)

    return 0

def plot_time_differences_CDF(time_differences):

    print "Plotting Time Diffences CDF"

    figs_path = './Figures/Inference_CDF/Time_Differences/'
    fig_name = 'Time_Differences.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    values = np.sort(time_differences)
    p = 1. * np.arange(len(values)) / (len(values) - 1)
    plt.plot(values, p)
    plt.grid()
    plt.title("Time Difference Between Video Session and BISmark Bitrate Data")
    plt.ylabel("P(x)")
    plt.xlabel("Time [days]")

    plt.savefig(figs_path + fig_name, dpi=900)
    # plt.show()
    plt.close()

    return 0

def get_time_difference_between_closest_video_session_bitrate(bitrate_df, inference_df, target):

    print "Getting difference between closest video session time and BISmark down bitrate entry."

    bitrate_df.set_index(pd.DatetimeIndex(bitrate_df["Event_date"]), inplace=True)
    inference_df.set_index(pd.DatetimeIndex(inference_df["Event_date"]), inplace=True)

    bitrate_deployments = bitrate_df["deployment"].unique()
    inference_deployments = inference_df["deployment"].unique()

    inference_services = inference_df["service"].unique()

    matching_deployments = set(bitrate_deployments) & set(inference_deployments)

    matching_deployments = sorted(matching_deployments)

    differences_list = []

    for deployment in matching_deployments:
        for service in inference_services:
            down_capacity = []
            metric = []
            sub_inference_df = inference_df.loc[(inference_df["deployment"] == deployment) & (inference_df["service"] == service)]
            sub_bitrate_df = bitrate_df.loc[bitrate_df["deployment"] == deployment]

            try:
                start_date = sub_inference_df.index[0]

                startloc = sub_bitrate_df.index.get_loc(start_date, method="nearest")

                closest_date = datetime.strptime(sub_bitrate_df.iloc[startloc]["Event_date"], '%Y-%m-%d %H:%M:%S')

                difference = closest_date - start_date
                difference = difference.days

                differences_list.append(difference)

                # if startloc == endloc:
                #     if endloc == 0:
                #         sli = sub_bitrate_df[endloc:endloc + len(sub_inference_df["deployment"])]
                #         down_capacity = sli["inf_capacity"]
                #     else:
                #         sli = sub_bitrate_df[endloc - (len(sub_inference_df["deployment"])):endloc]
                #         down_capacity = sli["inf_capacity"]
                # elif (endloc - startloc) > len(sub_inference_df["deployment"]):
                #     for entry in sub_inference_df.index.values:
                #         loc = sub_bitrate_df.index.get_loc(entry, method="nearest")
                #         temp_value = sub_bitrate_df["inf_capacity"].iloc[loc]
                #         down_capacity.append(temp_value)
                # elif (endloc - startloc) < len(sub_inference_df["deployment"]):
                #     sli = sub_bitrate_df[startloc:endloc]
                #     down_capacity = sli["inf_capacity"]
                #     if len(down_capacity) < len(sub_inference_df["deployment"]):
                #         sli = sub_bitrate_df[startloc:startloc + len(sub_inference_df["deployment"])]
                #         down_capacity = sli["inf_capacity"]
                #         if len(down_capacity) < len(sub_inference_df["deployment"]):
                #             sli = sub_bitrate_df[0:0 + len(sub_inference_df["deployment"])]
                #             down_capacity = sli["inf_capacity"]
                #
                # metric = sub_inference_df["metric"].values
                #
                # if target == "resolution":
                #     metric_list = []
                #     for value in metric:
                #         metric_list.append(value)
                #     metric = metric_list
                #
                # # Make the down bitrates and inference arrays match.
                # if len(down_capacity) != len(metric):
                #     if len(down_capacity) > len(metric):
                #         down_capacity = down_capacity[:len(metric)]
                #     else:
                #         metric = metric[:len(down_capacity)]
                #
                # # plot_scatter_infer_vs_down_capacity_with_service(deployment, down_capacity, metric, target, service)
                #
                # if service == "youtube":
                #     youtube_metrics.extend(metric)
                #     youtube_bitrates.extend(down_capacity)
                # elif service == "amazon":
                #     amazon_metrics.extend(metric)
                #     amazon_bitrates.extend(down_capacity)
                # elif service == "twitch":
                #     twitch_metrics.extend(metric)
                #     twitch_bitrates.extend(down_capacity)
                # elif service == "netflix":
                #     netflix_metrics.extend(metric)
                #     netflix_bitrates.extend(down_capacity)

            except Exception as excp:
                print "Exception for " + deployment + " and " + service + ": " + str(excp)

    plot_time_differences_CDF(differences_list)

    return 0

def prepare_data_to_plot(bitrate_df, inference_df, target):

    bitrate_df.set_index(pd.DatetimeIndex(bitrate_df["Event_date"]), inplace=True)
    inference_df.set_index(pd.DatetimeIndex(inference_df["Event_date"]), inplace=True)

    bitrate_deployments = bitrate_df["deployment"].unique()
    inference_deployments = inference_df["deployment"].unique()

    matching_deployments = set(bitrate_deployments) & set(inference_deployments)

    matching_deployments = sorted(matching_deployments)

    for deployment in matching_deployments:

        down_bitrate = []
        metric = []
        sub_inference_df = inference_df.loc[inference_df["deployment"] == deployment]
        sub_bitrate_df = bitrate_df.loc[bitrate_df["deployment"] == deployment]

        try:
            start_date = sub_inference_df.index[0]
            end_date = sub_inference_df.index[-1]

            startloc = sub_bitrate_df.index.get_loc(start_date, method="nearest")
            endloc = sub_bitrate_df.index.get_loc(end_date, method="nearest")

            # Here we take a slice of the bitrate dataframe which corresponds to the
            # entries for video session in the inference data frame.
            # We take the closests entries to the video sesssions.
            # Please be aware that in some cases the close bitrate reading is months
            # before the video session
            if startloc == endloc:
                if endloc == 0:
                    sli = sub_bitrate_df[endloc:endloc + len(sub_inference_df["deployment"])]
                    down_bitrate = sli["Down_bitrate"]
                else:
                    sli = sub_bitrate_df[endloc - (len(sub_inference_df["deployment"])):endloc]
                    down_bitrate = sli["Down_bitrate"]
            elif (endloc - startloc) > len(sub_inference_df["deployment"]):
                for entry in sub_inference_df.index.values:
                    loc = sub_bitrate_df.index.get_loc(entry, method="nearest")
                    temp_value = sub_bitrate_df["Down_bitrate"].iloc[loc]
                    down_bitrate.append(temp_value)
            elif (endloc - startloc) < len(sub_inference_df["deployment"]):
                sli = sub_bitrate_df[startloc:endloc]
                down_bitrate = sli["Down_bitrate"]
                if len(down_bitrate) < len(sub_inference_df["deployment"]):
                    sli = sub_bitrate_df[startloc:startloc + len(sub_inference_df["deployment"])]
                    down_bitrate = sli["Down_bitrate"]
                    if len(down_bitrate) < len(sub_inference_df["deployment"]):
                        sli = sub_bitrate_df[0:0 + len(sub_inference_df["deployment"])]
                        down_bitrate = sli["Down_bitrate"]

            metric = sub_inference_df["metric"].values

            if target == "resolution":
                metric_list = []
                for value in metric:
                    metric_list.append(value)
                metric = metric_list

            # Make the down bitrates and inference arrays match.
            if len(down_bitrate) != len(metric):
                if len(down_bitrate) > len(metric):
                    down_bitrate = down_bitrate[:len(metric)]
                else:
                    metric = metric[:len(down_bitrate)]

            plot_scatter_infer_vs_down_bitrate(deployment, down_bitrate, metric, target)

        except Exception as excp:
                print "Exception for " + deployment + ": " + str(excp)

    return 0

def get_inferred_capacity(bitrate_df):

    print "Inferring Capacity from the 95 percentile of down bitrates per deployment."

    deployments = bitrate_df["deployment"].unique()
    all_bitrates = []
    for deployment in deployments:
        bitrates_list = bitrate_df.loc[bitrate_df["deployment"] == deployment]["Down_bitrate"].values
        inferred_capacity = np.percentile(bitrates_list, 95)
        for entry in bitrates_list:
            all_bitrates.append(inferred_capacity)

    bitrate_df["inf_capacity"] = all_bitrates

    return bitrate_df

def merge_dataframe(bitrate_df, inference_df):

    master_df = pd.DataFrame(columns=["deployment", "down_capacity", "resolution"])

    bitrate_deployments = bitrate_df["deployment"].unique()
    inference_deployments = inference_df["deployment"].unique()

    matching_deployments = set(bitrate_deployments) & set(inference_deployments)
    matching_deployments = sorted(matching_deployments)

    deployments_lists = []
    resolutions = []
    down_capacities = []

    for deployment in matching_deployments:
        query_str = "deployment == '"+deployment+"'"

        tmp_bitrate_df = bitrate_df.query(query_str)
        tmp_inference_df = inference_df.query(query_str)

        inf_capacity = tmp_bitrate_df.iloc[0]["inf_capacity"]
        res_per_deployment = tmp_inference_df["metric"].mode()[0]

        deployments_lists.append(deployment)
        down_capacities.append(inf_capacity)
        resolutions.append(res_per_deployment)

    master_df["deployment"] = deployments_lists
    master_df["down_capacity"] = down_capacities
    master_df["resolution"] = resolutions

    master_df.to_csv("./CSVs/Resolution_per_deployment/res_per_deployment.csv")
    return 0

def main():

    print "Script Start"

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, required=True, help="Inference target: 'startup' or 'resolution'")
    parser.add_argument('-m', '--metric', type=str, required=True, help="Inference target: 'throughput' or 'capacity'")

    args = vars(parser.parse_args())

    target = args["target"]
    bis_metric = args["metric"]

    bitrate_df, metric_df = load_merge_dfs_by_time("./CSVs/By_Time/", target, with_service=True)
    # bitrate_df, metric_df = load_merge_dfs_by_time("./CSVs/By_Time/", target, with_service=False)

    if bis_metric == "capacity":
        bitrate_df = get_inferred_capacity(bitrate_df)
        if target == "resolution":
            merge_dataframe(bitrate_df, metric_df)

    # get_time_difference_between_closest_video_session_bitrate(bitrate_df, metric_df, target)
    # plot_CDF_target(metric_df, target)
    # prepare_data_to_plot(bitrate_df, metric_df, target)

    prepare_data_to_plot_with_service(bitrate_df, metric_df, target, bis_metric)

    # prepare_data_to_plot_with_service_inf_capacity(bitrate_df, metric_df, target)
    # load_CSVs('./CSVs/')

    print "Script Completed"

    return 0


if __name__ == "__main__":
    main()