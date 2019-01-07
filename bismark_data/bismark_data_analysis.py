import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import os
import csv

def mac_address_to_deployment_id(results_df):

    # mapping = np.genfromtxt('./CSVs/deployment_mac.csv', dtype=None)

    with open('./CSVs/deployment_mac.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mapping_dict = dict((rows[1], rows[0]) for rows in reader)


    mac_address_list = results_df.index.values
    deployment_ids = []

    for mac_address in mac_address_list:
        deployment_id = mapping_dict.get(mac_address, "NA")
        deployment_ids.append(deployment_id)
        # if mac_address in mapping_dict.keys():
        #     deployment_ids.append(mapping_dict.get(mac_address))

    results_df["deployment_id"] = deployment_ids

    plot_bitrate_avg_per_deployment(results_df)

    percentiles = [50, 75, 85, 90]

    for perc in percentiles:
        plot_bitrate_percentiles_per_deployment(results_df, perc)

    export_df_to_CSV(results_df)

    return 0

def export_df_to_CSV(results_df):

    csvs_path = './CSVs/'
    csv_filename = 'Bitrate_per_deployment.csv'

    if not os.path.exists(csvs_path):
        os.makedirs(csvs_path)

    results_df.to_csv(csvs_path + csv_filename)

    return 0

def plot_bitrate_percentiles_per_deployment(data_df, percentile):
    print "Plotting Bitrate Percentiles "+str(percentile)+" per Deployment"

    figs_path = './Figures/Bitrate_Percentiles/'
    fig_name = 'Up_Down_' + str(percentile) + '_Bitrate_per_deployment.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    # deployments = data_df.index.values
    deployments = data_df["deployment_id"].values

    up_perc_col = 'Up_Perc_' + str(percentile)
    down_perc_col = 'Down_Perc_' + str(percentile)

    up_perc_data = data_df[up_perc_col].values
    down_perc_data = data_df[down_perc_col].values

    up_data = []
    down_data = []

    for up_value in up_perc_data:
        up_data.append(up_value / 1000)

    for down_value in down_perc_data:
        down_data.append(down_value / 1000)

    temp_df = pd.DataFrame(columns=["deployment_id", "Avg_Up", "Avg_Down"])

    temp_df["deployment_id"] = deployments
    temp_df["Avg_Up"] = up_data
    temp_df["Avg_Down"] = down_data



    temp_df = temp_df.sort(columns='Avg_Down', ascending=False)

    deployments = temp_df.deployment_id.values
    up_data = temp_df.Avg_Up.values
    down_data = temp_df.Avg_Down.values

    ind = np.arange(len(deployments))
    width = 0.35

    fig, ax = plt.subplots()

    ups = ax.bar(ind - width / 2, up_data, width, color='SkyBlue', label='Up')
    downs = ax.bar(ind + width / 2, down_data, width, color='IndianRed', label='Down')

    # Add some text for labels, title and custom x-axis tick labels.
    ax.set_ylabel('Bitrate [Mbps]')
    ax.set_title('Up/Down Bitrate ' + str(percentile) + ' Percentile per Deployment')
    ax.set_xticks(ind)
    ax.set_xticklabels(deployments)
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation='vertical', fontsize=7)
    # plt.xticks(rotation=90)
    plt.grid()

    # plt.show()
    plt.savefig(figs_path + fig_name, dpi=900)
    plt.close()

    return 0

def plot_bitrate_avg_per_deployment(data_df):
    print "Plotting Bitrate Average per Deployment."

    figs_path = './Figures/Birate_Avg/'
    fig_name = 'Avg_Up_Down_Bitrate_per_deployment.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    # deployments = data_df.index.values
    deployments = data_df["deployment_id"].values

    up_avgs = []
    for up_entry in data_df.Avg_Up.values:
        up_avgs.append(up_entry / 1000)

    down_avgs = []
    for down_entry in data_df.Avg_Down.values:
        down_avgs.append(down_entry / 1000)

    temp_df = pd.DataFrame(columns=["deployment_id", "Avg_Up", "Avg_Down"])

    temp_df["deployment_id"] = deployments
    temp_df["Avg_Up"] = up_avgs
    temp_df["Avg_Down"] = down_avgs



    temp_df = temp_df.sort(columns='Avg_Down', ascending=False)

    deployments = temp_df.deployment_id.values
    up_avgs = temp_df.Avg_Up.values
    down_avgs = temp_df.Avg_Down.values


    ind = np.arange(len(deployments))
    width = 0.35

    fig, ax = plt.subplots()

    ax.bar(ind - width / 2, up_avgs, width, color='SkyBlue', label='Up')
    ax.bar(ind + width / 2, down_avgs, width, color='IndianRed', label='Down')

    # Add some text for labels, title and custom x-axis tick labels.
    ax.set_ylabel('Bitrate [Mbps]')
    ax.set_title('Avg Up and Down Bitrate per Deployment')
    ax.set_xticks(ind)
    ax.set_xticklabels(deployments)
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation='vertical', fontsize=7)
    # plt.xticks(rotation=70)
    plt.grid()

    # plt.show()
    plt.savefig(figs_path + fig_name, dpi=900)
    plt.close()

    return 0

def plot_by_deployment(data_df):

    print "Plotting bitrate per deployment."

    deployments = data_df.index.values

    up_avgs = []

    for up_entry in data_df.Avg_Up.values:
        up_avgs.append(up_entry/1000)

    down_avgs = []
    for down_entry in data_df.Avg_Down.values:
        down_avgs.append(down_entry/1000)

    ind = np.arange(len(deployments))
    width = 0.35

    fig, ax = plt.subplots()

    ups = ax.bar(ind - width / 2, up_avgs, width, color='SkyBlue', label='Up')
    downs = ax.bar(ind + width / 2, down_avgs, width, color='IndianRed', label='Down')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Bitrate [Mbps]')
    ax.set_title('Avg Up and Down Bitrate per Deployment')
    ax.set_xticks(ind)
    ax.set_xticklabels(deployments)
    ax.legend()
    plt.xticks(rotation=70)

    plt.show()
    # plt.savefig('./Figures/Avg_Bitrate_Up_Down.png', dpi=900)
    plt.close()

    return 0

def plot_CDF_per_deployment(up_data, down_data, deployment):

    print "Creating Up/Down CDFs for deployment "+str(deployment)

    figs_path = "./Figures/CDFs/"
    fig_up_filename = deployment.replace(":", "_") + "_CDF_up.png"
    fig_down_filename = deployment.replace(":", "_") + "_CDF_down.png"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    # Up CDF
    data = []
    for entry in up_data:
        data.append(entry/1000)

    data = np.sort(data)
    p = 1. * np.arange(len(data)) / (len(data) - 1)
    plt.plot(data, p)
    plt.grid()
    plt.title("Up Bitrate CDF for " + str(deployment))
    plt.ylabel("P(x)")
    plt.xlabel("Up Bitrate [Mbps]")
    plt.savefig(figs_path + fig_up_filename, dpi=900)
    # plt.show()
    plt.close()

    # Down CDF
    data = []
    for entry in down_data:
        data.append(entry / 1000)

    data = np.sort(data)
    p = 1. * np.arange(len(data)) / (len(data) - 1)
    plt.plot(data, p)
    plt.grid()
    plt.title("Down Bitrate CDF for " + str(deployment))
    plt.ylabel("P(x)")
    plt.xlabel("Down Bitrate [Mbps]")
    plt.savefig(figs_path + fig_down_filename, dpi=900)
    # plt.show()
    plt.close()

    return 0

def prepare_data_plot_CDF(bitrate_all_df):

    print "Preparing Data to be plot CDF per deployment "

    for index, row in bitrate_all_df.iterrows():
        deployment = index
        up_data = row["Up"]
        down_data = row["Down"]
        plot_CDF_per_deployment(up_data, down_data, deployment)


    return 0

def plot_groups_bars(grouped_df, percentile):

    # Settings for labels in the plot
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height

    figs_path = "./Figures/Groups/"

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    fig, ax = subplots()
    grouped_df.groupby("Group").count().plot(kind='bar', ax=ax)
    # ax.legend(["Deployments"])

    groups_list = ["Group 1", "Group 2", "Group 3", "Group 4", "Group 5", "Group 6"]
    plt.xticks(np.arange(6), groups_list)
    plt.grid()


    textstr = '\n'.join((
        'Group 1: 0 - 50 Mbps',
        'Group 2: 51 - 100 Mbps',
        'Group 3: 101 - 150 Mbps',
        'Group 4: 151 - 200 Mbps',
        'Group 5: 201 - 250 Mbps',
        'Group 6: 251+ Mbps'))

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)

    ax.text(right, top, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props, horizontalalignment='right')


    if percentile is not None:
        plt.title("Deployments Groups by Down Bitrate "+str(percentile)+" Percentile")
        fig_filename = "Groups_by_Down_"+str(percentile)+"_Perc.png"
    else:
        plt.title("Deployments Groups by Down Bitrate Average")
        fig_filename = "Groups_by_Down_Avg.png"

    plt.ylabel("Number of Deployments")
    plt.xlabel("")
    plt.xticks(rotation=0)
    plt.savefig(figs_path + fig_filename, dpi=900)
    # plt.show()
    plt.close()

    # plt.clf()
    # ax = grouped_df.groupby("Group").count().plot(kind='bar')
    #
    # groups_list = ["Group 1", "Group 2", "Group 3", "Group 4", "Group 5", "Group 6"]
    #
    # plt.xticks(np.arange(6), groups_list)
    # plt.grid()
    # ax.legend(["Group 1: 0 - 50 Mbps", "Group 2: 51 - 100 Mbps", "Group 3: 101 - 150 Mbps", "Group 4: 151 - 200 Mbps", "Group 5: 201 - 250 Mbps", "Group 6: 251+ Mbps"])
    # plt.title("Deployments Groups by Down Bitrate Average")
    # plt.ylabel("Down Bitrate [Mbps]")
    # plt.xlabel("Group")
    # plt.xticks(rotation=0)
    # # plt.savefig(figs_path + fig_down_filename, dpi=900)
    # plt.show()
    # plt.close()

    return 0

def group_deployments_by_percentile(deployments_df, percentile):

    print "Grouping deployments by "+str(percentile)+" Percentile"

    # Groups
    #  0 - 50 Mbps      1
    # 51 - 100 Mbpbs    2
    # 101 - 150 Mbps    3
    # 151 - 200 Mbps    4
    # 201 - 250 Mbps    5
    # 251 Mbps +        6

    # for column in deployments_df:
    #     deployments_df[column] = deployments_df[column].div(1000)

    up_col_tag = "Up_Perc_"+str(percentile)
    down_col_tag = "Down_Perc_"+str(percentile)

    deployments_avgs_df = pd.DataFrame(columns=["Perc_Up","Perc_Down","Group"])
    deployments_avgs_df["deployment"] = deployments_df.index
    deployments_avgs_df["Perc_Up"] = deployments_df[up_col_tag].values
    deployments_avgs_df["Perc_Down"] = deployments_df[down_col_tag].values

    for index, row in deployments_avgs_df.iterrows():
        if row["Perc_Down"] > 0 and row["Perc_Down"] <= 50:
            deployments_avgs_df.loc[index, "Group"] = 1
            # row["Group"] = 1
        if row["Perc_Down"] > 50 and row["Perc_Down"] <= 100:
            deployments_avgs_df.loc[index, "Group"] = 2
            # row["Group"] = 2
        if row["Perc_Down"] > 100 and row["Perc_Down"] <= 150:
            deployments_avgs_df.loc[index, "Group"] = 3
            # row["Group"] = 3
        if row["Perc_Down"] > 150 and row["Perc_Down"] <= 200:
            deployments_avgs_df.loc[index, "Group"] = 4
            # row["Group"] = 4
        if row["Perc_Down"] > 200 and row["Perc_Down"] <= 250:
            deployments_avgs_df.loc[index, "Group"] = 5
            # row["Group"] = 5
        if row["Perc_Down"] > 250:
            deployments_avgs_df.loc[index, "Group"] = 6
            # row["Group"] = 6

    g1 = deployments_avgs_df.groupby(["Group", "deployment"]).count()
    g1 = g1.reset_index()

    g1 = g1.drop(labels=['Perc_Up','Perc_Down'], axis=1)

    # group0_50 = deployments_df.loc[(deployments_df['Avg_Down'] > 0) & (deployments_df['Avg_Down'] <= 50)]
    # group51_100 = deployments_df.loc[(deployments_df['Avg_Down'] > 50) & (deployments_df['Avg_Down'] <= 100)]
    # group101_150 = deployments_df.loc[(deployments_df['Avg_Down'] > 100) & (deployments_df['Avg_Down'] <= 150)]
    # group151_200 = deployments_df.loc[(deployments_df['Avg_Down'] > 150) & (deployments_df['Avg_Down'] <= 200)]
    # group201_250 = deployments_df.loc[(deployments_df['Avg_Down'] > 200) & (deployments_df['Avg_Down'] <= 250)]
    # group251_plus = deployments_df.loc[(deployments_df['Avg_Down'] > 250)]

    plot_groups_bars(g1, percentile)

    return 0

def group_deployments_by_average(deployments_df):

    print "Grouping deployments by average"

    # Groups
    #  0 - 50 Mbps      1
    # 51 - 100 Mbpbs    2
    # 101 - 150 Mbps    3
    # 151 - 200 Mbps    4
    # 201 - 250 Mbps    5
    # 251 Mbps +        6

    for column in deployments_df:
        deployments_df[column] = deployments_df[column].div(1000)


    deployments_avgs_df = pd.DataFrame(columns=["Avg_Up","Avg_Down","Group"])
    deployments_avgs_df["deployment"] = deployments_df.index
    deployments_avgs_df["Avg_Up"] = deployments_df["Avg_Up"].values
    deployments_avgs_df["Avg_Down"] = deployments_df["Avg_Down"].values

    for index, row in deployments_avgs_df.iterrows():
        if row["Avg_Down"] > 0 and row["Avg_Down"] <= 50:
            deployments_avgs_df.loc[index, "Group"] = 1
            # row["Group"] = 1
        if row["Avg_Down"] > 50 and row["Avg_Down"] <= 100:
            deployments_avgs_df.loc[index, "Group"] = 2
            # row["Group"] = 2
        if row["Avg_Down"] > 100 and row["Avg_Down"] <= 150:
            deployments_avgs_df.loc[index, "Group"] = 3
            # row["Group"] = 3
        if row["Avg_Down"] > 150 and row["Avg_Down"] <= 200:
            deployments_avgs_df.loc[index, "Group"] = 4
            # row["Group"] = 4
        if row["Avg_Down"] > 200 and row["Avg_Down"] <= 250:
            deployments_avgs_df.loc[index, "Group"] = 5
            # row["Group"] = 5
        if row["Avg_Down"] > 250:
            deployments_avgs_df.loc[index, "Group"] = 6
            # row["Group"] = 6

    g1 = deployments_avgs_df.groupby(["Group", "deployment"]).count()
    g1 = g1.reset_index()

    g1 = g1.drop(labels=['Avg_Up','Avg_Down'], axis=1)

    # group0_50 = deployments_df.loc[(deployments_df['Avg_Down'] > 0) & (deployments_df['Avg_Down'] <= 50)]
    # group51_100 = deployments_df.loc[(deployments_df['Avg_Down'] > 50) & (deployments_df['Avg_Down'] <= 100)]
    # group101_150 = deployments_df.loc[(deployments_df['Avg_Down'] > 100) & (deployments_df['Avg_Down'] <= 150)]
    # group151_200 = deployments_df.loc[(deployments_df['Avg_Down'] > 150) & (deployments_df['Avg_Down'] <= 200)]
    # group201_250 = deployments_df.loc[(deployments_df['Avg_Down'] > 200) & (deployments_df['Avg_Down'] <= 250)]
    # group251_plus = deployments_df.loc[(deployments_df['Avg_Down'] > 250)]

    plot_groups_bars(g1, percentile=None)

    return 0

def get_avg_bitrate_per_deployment(bitrate_df):

    print "Computing Bitrate per deployment."

    results_df = pd.DataFrame()

    device_bitrate_dict = {}

    for row in bitrate_df.itertuples():
        if row.Avg <= 0:
            continue
        else:
            if row.Device_ID not in device_bitrate_dict.keys():
                device_bitrate_dict[row.Device_ID] = {
                    "Up": [],
                    "Down": [],
                    "Avg_Up": 0.0,
                    "Avg_Down": 0.0,
                    "Up_Perc_50": 0.0,
                    "Up_Perc_75": 0.0,
                    "Up_Perc_85": 0.0,
                    "Up_Perc_90": 0.0,
                    "Down_Perc_50": 0.0,
                    "Down_Perc_75": 0.0,
                    "Down_Perc_85": 0.0,
                    "Down_Perc_90": 0.0
                }
                if row.Direction == 'up':
                    device_bitrate_dict[row.Device_ID]['Up'].append(row.Avg)
                else:
                    device_bitrate_dict[row.Device_ID]['Down'].append(row.Avg)
            else:
                if row.Direction == 'up':
                    device_bitrate_dict[row.Device_ID]['Up'].append(row.Avg)
                else:
                    device_bitrate_dict[row.Device_ID]['Down'].append(row.Avg)


    for device in device_bitrate_dict:
        device_bitrate_dict[device]['Avg_Up'] = np.mean(device_bitrate_dict[device]['Up'])
        device_bitrate_dict[device]['Avg_Down'] = np.mean(device_bitrate_dict[device]['Down'])
        device_bitrate_dict[device]['Up_Perc_50'] = np.percentile(device_bitrate_dict[device]['Up'], 50)
        device_bitrate_dict[device]['Up_Perc_75'] = np.percentile(device_bitrate_dict[device]['Up'], 75)
        device_bitrate_dict[device]['Up_Perc_85'] = np.percentile(device_bitrate_dict[device]['Up'], 85)
        device_bitrate_dict[device]['Up_Perc_90'] = np.percentile(device_bitrate_dict[device]['Up'], 90)
        device_bitrate_dict[device]['Down_Perc_50'] = np.percentile(device_bitrate_dict[device]['Down'], 50)
        device_bitrate_dict[device]['Down_Perc_75'] = np.percentile(device_bitrate_dict[device]['Down'], 75)
        device_bitrate_dict[device]['Down_Perc_85'] = np.percentile(device_bitrate_dict[device]['Down'], 85)
        device_bitrate_dict[device]['Down_Perc_90'] = np.percentile(device_bitrate_dict[device]['Down'], 90)

    results_df = pd.DataFrame.from_dict(device_bitrate_dict, orient='index')

    # prepare_data_plot_CDF(results_df)


    results_df = results_df.drop(labels=['Up', 'Down'], axis=1)

    group_deployments_by_average(results_df)

    percentiles = [50, 75, 85, 90]
    for perc in percentiles:
        group_deployments_by_percentile(results_df, perc)

    # mac_address_to_deployment_id(results_df)

    # export_df_to_CSV(results_df)

    # plot_by_deployment(results_df)

    return results_df

def get_down_bitrate_by_date_per_deployment(bitrate_df):

    print "Computing down birate by time per deployment."

    temp_df = bitrate_df.drop(labels=["Source_IP", "Destination_IP", "Std", "Min", "Max", "Median"], axis=1)

    temp_df = temp_df.loc[(temp_df["Direction"] == "dw") & (temp_df["Avg"] > 0)]

    temp_df = temp_df.drop(labels=["Direction"], axis=1)

    temp_df["Avg"] = temp_df["Avg"].div(1000)

    down_bitrate_df = temp_df.sort_values(["Device_ID", "Event_date"])

    return down_bitrate_df

def get_down_dict_from_down_df(down_bitrate_df):

    print "Converting Down Bitrate Dataframe to Dictionary"
    down_dict = {}

    for row in down_bitrate_df.itertuples():
        if row.Device_ID not in down_dict.keys():
            down_dict[row.Device_ID] = {
                "Event_dates": [],
                "Down_bitrates": []
            }
            down_dict[row.Device_ID]["Event_dates"].append(row.Event_date)
            down_dict[row.Device_ID]["Down_bitrates"].append(row.Avg)
        else:
            down_dict[row.Device_ID]["Event_dates"].append(row.Event_date)
            down_dict[row.Device_ID]["Down_bitrates"].append(row.Avg)

    return down_dict

def plot_down_bitrate_timeseries_per_deployment(down_dict):

    print "Plotting down bitrate timeseries per deployment."

    figs_path = './Figures/DownBitrate_TimeSeries/'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    for device in down_dict:
        dates = down_dict[device]["Event_dates"]
        down_bitrates = down_dict[device]["Down_bitrates"]
        plt.plot(dates, down_bitrates)
        plt.grid()
        plt.title("Down Bitrate for " + str(device))
        plt.ylabel("Down Bitrate [Mbps]")
        plt.xlabel("Date")
        fig_filename = device.replace(":", "_") + ".png"
        plt.savefig(figs_path + fig_filename, dpi=900)
        # plt.show()
        plt.close()

    print "Plotting Time Series Completed"

    return 0

def export_down_df_to_csv(down_bitrate_df):

    csvs_path = './CSVs/'
    csv_filename = 'Down_bitrate_by_time.csv'

    if not os.path.exists(csvs_path):
        os.makedirs(csvs_path)

    down_bitrate_df.to_csv(csvs_path + csv_filename)

    return 0

def main():

    print "Script Start"

    print "Loading CSV File"

    bitrate_df = pd.read_csv('../Scripts/Capacity/CSVs/20181227_bitarate.csv')

    print "CSV Load Completed"

    down_bitrate_df = get_down_bitrate_by_date_per_deployment(bitrate_df)

    export_down_df_to_csv(down_bitrate_df)

    # down_dict = get_down_dict_from_down_df(down_bitrate_df)

    # plot_down_bitrate_timeseries_per_deployment(down_dict)

    # get_avg_bitrate_per_deployment(bitrate_df)

    # capacity_df = pd.read_csv('../Scripts/Capacity/capacity.csv')

    print "End of Script"

    return 0

if __name__ == "__main__":
  main()