import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
import pytz

def plot_metric_percentiles_per_deployment(data_df, percentile, target):
    print "Plotting "+str(target)+" Percentiles per Deployment"

    figs_path = './Figures/'+str(target)+'_Percentiles/'
    fig_name = str(target)+'_'+str(percentile) + 'percentile_per_deployment.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    deployments = data_df.index.values
    # deployments = data_df["deployment_id"].values

    perc_col = str(percentile)+'_perc'

    perc_col_data = data_df[perc_col].values

    # up_perc_col = 'Up_Perc_' + str(percentile)
    # down_perc_col = 'Down_Perc_' + str(percentile)
    #
    # up_perc_data = data_df[up_perc_col].values
    # down_perc_data = data_df[down_perc_col].values

    perc_data = []
    # down_data = []

    if target == 'startup':
        for entry in perc_col_data:
            perc_data.append(entry / 1000)

    temp_df = pd.DataFrame(columns=["deployment_id", "Avg_Metric"])

    temp_df["deployment_id"] = deployments

    if target == 'startup':
        temp_df["Avg_Metric"] = perc_data
    else:
        temp_df["Avg_Metric"] = perc_col_data

    if target == 'startup':
        temp_df = temp_df.sort(columns='Avg_Metric', ascending=True)
    else:
        temp_df = temp_df.sort(columns='Avg_Metric', ascending=False)

    deployments = temp_df.deployment_id.values

    if target == 'startup':
        perc_data = temp_df.Avg_Metric.values
    else:
        perc_col_data = temp_df.Avg_Metric.values

    # for down_value in down_perc_data:
    #     down_data.append(down_value / 1000)

    ind = np.arange(len(deployments))
    width = 0.75

    fig, ax = plt.subplots()

    if target == 'startup':
        ups = ax.bar(ind, perc_data, width, color='SkyBlue', label='Startup Time')
    else:
        ups = ax.bar(ind, perc_col_data, width, color='SkyBlue', label='Resolution')

    # ups = ax.bar(ind - width, up_data, width, color='SkyBlue', label='Up')
    # downs = ax.bar(ind + width, down_data, width, color='IndianRed', label='Down')

    # Add some text for labels, title and custom x-axis tick labels.
    if target == 'startup':
        ax.set_ylabel('Time [sec]')
    else:
        ax.set_ylabel('Resolution [p]')
    # ax.set_ylabel('Bitrate [Mbps]')

    ax.set_title(str(target) +" "+ str(percentile) + ' Percentile per Deployment')
    ax.set_xticks(ind)
    ax.set_xticklabels(deployments)
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation='vertical', fontsize=6)
    # plt.xticks(rotation=45)
    plt.grid()

    # plt.show()
    plt.savefig(figs_path + fig_name, dpi=900)
    plt.close()

    return 0

def plot_metric_avg_per_deployment(data_df, target):
    print "Plotting "+str(target)+" Average per Deployment."

    figs_path = './Figures/'+str(target)+'_Avg/'
    fig_name = str(target)+'Avg_per_deployment.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    deployments = data_df.index.values
    # deployments = data_df["deployment_id"].values

    metric_avg_values = data_df.avg.values

    if target == 'startup':
        avgs = []
        for up_entry in metric_avg_values:
            avgs.append(up_entry / 1000)

    temp_df = pd.DataFrame(columns=["deployment_id", "Avg_Metric"])

    temp_df["deployment_id"] = deployments

    if target == 'startup':
        temp_df["Avg_Metric"] = avgs
    else:
        temp_df["Avg_Metric"] = metric_avg_values


    if target == 'startup':
        temp_df = temp_df.sort(columns='Avg_Metric', ascending=True)
    else:
        temp_df = temp_df.sort(columns='Avg_Metric', ascending=False)

    deployments = temp_df.deployment_id.values


    if target == 'startup':
        avgs = temp_df.Avg_Metric.values
    else:
        metric_avg_values = temp_df.Avg_Metric.values

    # down_avgs = []
    # for down_entry in data_df.Avg_Down.values:
    #     down_avgs.append(down_entry / 1000)

    ind = np.arange(len(deployments))
    width = 0.75

    fig, ax = plt.subplots()


    if target == 'startup':
        ups = ax.bar(ind, avgs, width, color='SkyBlue', label='Avg Startup Time')
    else:
        ups = ax.bar(ind, metric_avg_values, width, color='SkyBlue', label='Avg Resolution')


    # downs = ax.bar(ind + width / 2, down_avgs, width, color='IndianRed', label='Down')

    # Add some text for labels, title and custom x-axis tick labels.
    if target == 'startup':
        ax.set_ylabel('Time [sec]')
    else:
        ax.set_ylabel('Resolution [p]')

    ax.set_title('Avg '+str(target)+' per Deployment')
    ax.set_xticks(ind)
    ax.set_xticklabels(deployments)
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation='vertical', fontsize=6)
    # plt.xticks(rotation=45)
    plt.grid()

    # plt.show()
    plt.savefig(figs_path + fig_name, dpi=900)
    plt.close()

    return 0

def convert_to_df_export_CSV(inference_stats_dict, target):

    csv_path = './CSVs/'+str(target)+'/'
    csv_filename = str(target)+'_stats.csv'

    if not os.path.exists(csv_path):
        os.makedirs(csv_path)


    pre_dict_to_df = {}

    for deployment in inference_stats_dict:
        if deployment not in pre_dict_to_df.keys():
            pre_dict_to_df[deployment] = {
                "avg": inference_stats_dict[deployment]["all"]["target_avg"],
                "50_perc": inference_stats_dict[deployment]["all"]["target_50_perc"],
                "75_perc": inference_stats_dict[deployment]["all"]["target_75_perc"],
                "85_perc": inference_stats_dict[deployment]["all"]["target_85_perc"],
                "90_perc": inference_stats_dict[deployment]["all"]["target_90_perc"],
            }

    inference_stats_df = pd.DataFrame.from_dict(pre_dict_to_df, orient='index')

    plot_metric_avg_per_deployment(inference_stats_df, target)

    percentiles = [50, 75, 85, 90]

    for perc in percentiles:
        plot_metric_percentiles_per_deployment(inference_stats_df, perc, target)


    # To export to CSV
    # inference_stats_df.to_csv(csv_path+csv_filename)

    return 0

def plot_inference_stats(deployments, avgs, perc_50s, perc_75s, perc_85s, perc_90s, target):

    print "Plotting "+str(target)+" Stats"

    figs_path = './Figures/'+str(target)+'/'
    fig_name = str(target)+'stats_per_deployment.png'

    if not os.path.exists(figs_path):
        os.makedirs(figs_path)

    avgs[:] = [x / 1000 for x in avgs]
    perc_50s[:] = [x / 1000 for x in perc_50s]
    perc_75s[:] = [x / 1000 for x in perc_75s]
    perc_85s[:] = [x / 1000 for x in perc_85s]
    perc_90s[:] = [x / 1000 for x in perc_90s]

    ind = np.arange(len(deployments))
    width = 0.35

    fig, ax = plt.subplots()

    ax.bar(ind - width / 5, avgs, width, color='SkyBlue', label='Avg')
    ax.bar(ind + width / 5, perc_50s, width, color='IndianRed', label='50 Perc')
    ax.bar(ind + width / 5, perc_75s, width, color='green', label='75 Perc')
    ax.bar(ind + width / 5, perc_85s, width, color='yellow', label='85 Perc')
    ax.bar(ind + width / 5, perc_90s, width, color='black', label='90 Perc')

    # Add some text for labels, title and custom x-axis tick labels.
    ax.set_ylabel('Time [secs]')
    ax.set_title(str(target) + ' Inference Stats per Deployment')
    ax.set_xticks(ind)
    ax.set_xticklabels(deployments)
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation='vertical', fontsize=7)
    # plt.xticks(rotation=90)
    plt.grid()

    plt.show()
    # plt.savefig(figs_path + fig_name, dpi=900)
    plt.close()

    return 0

def get_stats_to_plot(inference_stats_dictionary, target):

    # df_inference_stats = pd.DataFrame.from_dict(inference_stats_dictionary, orient='index')

    deployments = []
    avgs = []
    perc_50s = []
    perc_75s = []
    perc_85s = []
    perc_90s = []

    for deployment in inference_stats_dictionary:
        deployments.append(deployment)
        avgs.append(inference_stats_dictionary[deployment]["all"]["target_avg"])
        perc_50s.append(inference_stats_dictionary[deployment]["all"]["target_50_perc"])
        perc_75s.append(inference_stats_dictionary[deployment]["all"]["target_75_perc"])
        perc_85s.append(inference_stats_dictionary[deployment]["all"]["target_85_perc"])
        perc_90s.append(inference_stats_dictionary[deployment]["all"]["target_90_perc"])


    plot_inference_stats(deployments, avgs, perc_50s, perc_75s, perc_85s, perc_90s, target)

    return 0

def get_target_all_deployments(inference_dir, target):
    print "Getting "+target+" inference for all deployments."

    inference_stats_dict = {}

    master_dataset = []
    prev_deployment = None
    stats_per_deployment = []

    # for root,dirs,files in os.walk(inference_dir + '/' +deployment):
    for root, dirs, files in os.walk(inference_dir):
        for file in files:
            if file.startswith('.'):
                continue

            deployment = root.split('/')[-2]
            service = root.split('/')[-1]

            inference_pickle = pd.read_pickle(root + '/' + file)

            tag = inference_pickle.columns.values[-1]

            dataset = inference_pickle[tag].values
            master_dataset.extend(dataset)

            if prev_deployment is None:
                prev_deployment = deployment

            target_avg = np.average(dataset)
            target_50_perc = np.percentile(dataset, 50)
            target_75_perc = np.percentile(dataset, 75)
            target_85_perc = np.percentile(dataset, 85)
            target_90_perc = np.percentile(dataset, 90)

            if deployment not in inference_stats_dict.keys():
                inference_stats_dict[deployment] = {}
                if service not in inference_stats_dict[deployment].keys():
                    inference_stats_dict[deployment][service] = {
                        "target_avg": target_avg,
                        "target_50_perc": target_50_perc,
                        "target_75_perc": target_75_perc,
                        "target_85_perc": target_85_perc,
                        "target_90_perc": target_90_perc
                    }
            elif service not in inference_stats_dict[deployment].keys():
                inference_stats_dict[deployment][service] = {
                    "target_avg": target_avg,
                    "target_50_perc": target_50_perc,
                    "target_75_perc": target_75_perc,
                    "target_85_perc": target_85_perc,
                    "target_90_perc": target_90_perc
                }


            if prev_deployment == deployment:
                stats_per_deployment.extend(dataset)
            else:
                inference_stats_dict[prev_deployment]["all"] = {
                    "target_avg": np.average(stats_per_deployment),
                    "target_50_perc": np.percentile(stats_per_deployment, 50),
                    "target_75_perc": np.percentile(stats_per_deployment, 70),
                    "target_85_perc": np.percentile(stats_per_deployment, 85),
                    "target_90_perc": np.percentile(stats_per_deployment, 90),
                }
                prev_deployment = deployment
                stats_per_deployment = []
                stats_per_deployment.extend(dataset)


    inference_stats_dict[deployment]["all"] = {
        "target_avg": np.average(stats_per_deployment),
        "target_50_perc": np.percentile(stats_per_deployment, 50),
        "target_75_perc": np.percentile(stats_per_deployment, 70),
        "target_85_perc": np.percentile(stats_per_deployment, 85),
        "target_90_perc": np.percentile(stats_per_deployment, 90),
    }



    inference_stats_dict["all"] = {}
    inference_stats_dict["all"]["all"] = {
        "target_avg": np.average(master_dataset),
        "target_50_perc": np.percentile(master_dataset, 50),
        "target_75_perc": np.percentile(master_dataset, 75),
        "target_85_perc": np.percentile(master_dataset, 85),
        "target_90_perc": np.percentile(master_dataset, 90)
    }

    convert_to_df_export_CSV(inference_stats_dict, target)
    # get_stats_to_plot(inference_stats_dict,target)

    return 0

def get_target_per_deployment_with_service_video_session(inference_dir, target):

    print "Getting "+target+" inference per deployment with service and video session ID"

    inference_stats_dict = {}
    prev_deployment = None
    all_metrics = []
    all_timestamps = []
    all_session_ids = []
    metric_per_deployment = []
    timestamps_per_deployment = []
    session_ids_per_deployment = []

    for root, dirs, files in os.walk(inference_dir):
        for file in files:
            if file.startswith('.') or not file.endswith(".pickle"):
                continue

            deployment = root.split('/')[-2]
            service = root.split('/')[-1]

            inference_pickle = pd.read_pickle(root + '/' + file)

            metric = inference_pickle.columns.values[-1]

            # From milliseconds to seconds if the target is startup
            # If the target is resolution we remove the values for the 1st minute
            if target == "startup":
                inference_pickle[metric] = inference_pickle[metric].div(1000)
            else:
                inference_pickle = inference_pickle.query("relative_timestamp > 60")

            dataset = inference_pickle[metric].values
            timestamps = inference_pickle["absolute_timestamp"].values
            session_ids = inference_pickle["session_id"].values

            all_metrics.extend(dataset)
            all_timestamps.extend(timestamps)
            all_session_ids.extend(session_ids)

            if prev_deployment is None:
                prev_deployment = deployment

            if deployment not in inference_stats_dict.keys():
                inference_stats_dict[deployment] = {}
                if service not in inference_stats_dict[deployment].keys():
                    inference_stats_dict[deployment][service] = {
                        "metrics": dataset,
                        "timestamps": timestamps,
                        "session_ids": session_ids
                    }
            elif service not in inference_stats_dict[deployment].keys():
                inference_stats_dict[deployment][service] = {
                    "metrics": dataset,
                    "timestamps": timestamps,
                    "session_ids": session_ids
                }

            if prev_deployment == deployment:
                metric_per_deployment.extend(dataset)
                timestamps_per_deployment.extend(timestamps)
            else:
                inference_stats_dict[prev_deployment]["all_services"] = {
                    "metrics": dataset,
                    "timestamps": timestamps,
                    "session_ids": session_ids
                }
                prev_deployment = deployment
                metric_per_deployment = []
                timestamps_per_deployment = []

    inference_stats_dict[deployment]["all_services"] = {
        "metrics": metric_per_deployment,
        "timestamps": timestamps_per_deployment,
        "session_ids": session_ids_per_deployment
    }

    inference_stats_dict["all_deployments"] = {}
    inference_stats_dict["all_deployments"]["all_services"] = {
        "metrics": all_metrics,
        "timestamps": all_timestamps,
        "session_ids": all_session_ids
    }

    return inference_stats_dict

# def get_target_per_deployment_with_service_video_session_relative_time(inference_dir, target):
#
#     print "Getting "+target+" inference per deployment with service and video session ID"
#
#     inference_stats_dict = {}
#     prev_deployment = None
#     all_metrics = []
#     all_timestamps = []
#     all_session_ids = []
#     metric_per_deployment = []
#     timestamps_per_deployment = []
#     session_ids_per_deployment = []
#     relative_timestamps = []
#
#     for root, dirs, files in os.walk(inference_dir):
#         for file in files:
#             if file.startswith('.') or not file.endswith(".pickle"):
#                 continue
#
#             deployment = root.split('/')[-2]
#             service = root.split('/')[-1]
#
#             inference_pickle = pd.read_pickle(root + '/' + file)
#
#             metric = inference_pickle.columns.values[-1]
#
#             # From milliseconds to seconds
#             if target == "startup":
#                 inference_pickle[metric] = inference_pickle[metric].div(1000)
#             else:
#                 inference_pickle = inference_pickle.query("relative_timestamp > 60")
#                 inference_pickle[metric] = inference_pickle[metric]
#
#
#             dataset = inference_pickle[metric].values
#             timestamps = inference_pickle["absolute_timestamp"].values
#             session_ids = inference_pickle["session_id"].values
#             relative_timestamps = inference_pickle["relative_timestamp"].values
#
#             all_metrics.extend(dataset)
#             all_timestamps.extend(timestamps)
#             all_session_ids.extend(session_ids)
#
#             if prev_deployment is None:
#                 prev_deployment = deployment
#
#             if deployment not in inference_stats_dict.keys():
#                 inference_stats_dict[deployment] = {}
#                 if service not in inference_stats_dict[deployment].keys():
#                     inference_stats_dict[deployment][service] = {
#                         "metrics": dataset,
#                         "timestamps": timestamps,
#                         "session_ids": session_ids,
#                         "relative_timestamps": relative_timestamps
#                     }
#             elif service not in inference_stats_dict[deployment].keys():
#                 inference_stats_dict[deployment][service] = {
#                     "metrics": dataset,
#                     "timestamps": timestamps,
#                     "session_ids": session_ids,
#                     "relative_timestamps": relative_timestamps
#                 }
#
#             if prev_deployment == deployment:
#                 metric_per_deployment.extend(dataset)
#                 timestamps_per_deployment.extend(timestamps)
#             else:
#                 inference_stats_dict[prev_deployment]["all_services"] = {
#                     "metrics": dataset,
#                     "timestamps": timestamps,
#                     "session_ids": session_ids,
#                     "relative_timestamps": relative_timestamps
#                 }
#                 prev_deployment = deployment
#                 metric_per_deployment = []
#                 timestamps_per_deployment = []
#
#     inference_stats_dict[deployment]["all_services"] = {
#         "metrics": metric_per_deployment,
#         "timestamps": timestamps_per_deployment,
#         "session_ids": session_ids_per_deployment,
#         "relative_timestamps": relative_timestamps
#     }
#
#     inference_stats_dict["all_deployments"] = {}
#     inference_stats_dict["all_deployments"]["all_services"] = {
#         "metrics": all_metrics,
#         "timestamps": all_timestamps,
#         "session_ids": all_session_ids,
#         "relative_timestamps": relative_timestamps
#     }
#
#     return inference_stats_dict

def get_target_per_deployment(inference_dir, target):

    print "Getting "+target+" inference per deployment."

    inference_stats_dict = {}
    prev_deployment = None
    all_metrics = []
    all_timestamps = []
    metric_per_deployment = []
    timestamps_per_deployment = []

    for root, dirs, files in os.walk(inference_dir):
        for file in files:
            if file.startswith('.') or not file.endswith(".pickle"):
                continue

            deployment = root.split('/')[-2]
            service = root.split('/')[-1]

            inference_pickle = pd.read_pickle(root + '/' + file)

            metric = inference_pickle.columns.values[-1]

            # From milliseconds to seconds
            if target == "startup":
                inference_pickle[metric] = inference_pickle[metric].div(1000)
            else:
                inference_pickle[metric] = inference_pickle[metric]

            dataset = inference_pickle[metric].values
            timestamps = inference_pickle["absolute_timestamp"].values

            all_metrics.extend(dataset)
            all_timestamps.extend(timestamps)

            if prev_deployment is None:
                prev_deployment = deployment

            if deployment not in inference_stats_dict.keys():
                inference_stats_dict[deployment] = {}
                if service not in inference_stats_dict[deployment].keys():
                    inference_stats_dict[deployment][service] = {
                        "metrics": dataset,
                        "timestamps": timestamps
                        # "target_avg": target_avg,
                        # "target_50_perc": target_50_perc,
                        # "target_75_perc": target_75_perc,
                        # "target_85_perc": target_85_perc,
                        # "target_90_perc": target_95_perc
                    }
            elif service not in inference_stats_dict[deployment].keys():
                inference_stats_dict[deployment][service] = {
                    "metrics": dataset,
                    "timestamps": timestamps
                    # "target_avg": target_avg,
                    # "target_50_perc": target_50_perc,
                    # "target_75_perc": target_75_perc,
                    # "target_85_perc": target_85_perc,
                    # "target_90_perc": target_95_perc
                }

            if prev_deployment == deployment:
                metric_per_deployment.extend(dataset)
                timestamps_per_deployment.extend(timestamps)
            else:
                inference_stats_dict[prev_deployment]["all_services"] = {
                    "metrics": dataset,
                    "timestamps": timestamps
                    # "target_avg": np.average(stats_per_deployment),
                    # "target_50_perc": np.percentile(stats_per_deployment, 50),
                    # "target_75_perc": np.percentile(stats_per_deployment, 70),
                    # "target_85_perc": np.percentile(stats_per_deployment, 85),
                    # "target_90_perc": np.percentile(stats_per_deployment, 90)
                }
                prev_deployment = deployment
                metric_per_deployment = []
                timestamps_per_deployment = []
                # stats_per_deployment.extend(dataset)

    inference_stats_dict[deployment]["all_services"] = {
        "metrics": metric_per_deployment,
        "timestamps": timestamps_per_deployment
        # "target_avg": np.average(stats_per_deployment),
        # "target_50_perc": np.percentile(stats_per_deployment, 50),
        # "target_75_perc": np.percentile(stats_per_deployment, 70),
        # "target_85_perc": np.percentile(stats_per_deployment, 85),
        # "target_90_perc": np.percentile(stats_per_deployment, 90),
    }

    inference_stats_dict["all_deployments"] = {}
    inference_stats_dict["all_deployments"]["all_services"] = {
        "metrics": all_metrics,
        "timestamps": all_timestamps
        # "target_avg": np.average(master_dataset),
        # "target_50_perc": np.percentile(master_dataset, 50),
        # "target_75_perc": np.percentile(master_dataset, 75),
        # "target_85_perc": np.percentile(master_dataset, 85),
        # "target_90_perc": np.percentile(master_dataset, 90)
    }

    return inference_stats_dict

def format_inference_stats_dict(inference_stats_dict):

    print "Creating dictionary with inferred metric with timestamp."

    dict_to_convert = {}

    for deployment in inference_stats_dict:
        if deployment == "all_deployments":
            continue
        else:
            dict_to_convert[deployment] = {}
            dict_to_convert[deployment] = {
                "metrics": inference_stats_dict[deployment]["all_services"]["metrics"],
                "timestamps": inference_stats_dict[deployment]["all_services"]["timestamps"]
            }

    return dict_to_convert

def format_inference_stats_dict_with_service(inference_stats_dict):

    print "Creating dictionary with inferred metric with timestamp."

    dict_to_convert = {}

    for deployment in inference_stats_dict:
        if deployment == "all_deployments":
            continue
        else:
            dict_to_convert[deployment] = {
                "metrics": [],
                "timestamps": [],
                "service": []
            }
            for service in inference_stats_dict[deployment]:
                if service == "all_services":
                    continue
                else:
                    metric_list = []
                    timestamp_list = []
                    service_list = []

                    metric_list = inference_stats_dict[deployment][service]["metrics"]
                    timestamp_list = inference_stats_dict[deployment][service]["timestamps"]
                    for entry in metric_list:
                        service_list.append(service)

                    dict_to_convert[deployment]["metrics"].extend(metric_list)
                    dict_to_convert[deployment]["timestamps"].extend(timestamp_list)
                    dict_to_convert[deployment]["service"].extend(service_list)

                    # dict_to_convert[deployment] = {
                    #     "metrics": dict_to_convert[deployment]["metrics"].extend(metric_list),
                    #     "timestamps": dict_to_convert[deployment]["timestamps"].extend(timestamp_list),
                    #     "service": dict_to_convert[deployment]["service"].extend(service_list)
                    # }

            print "\n"

    return dict_to_convert

def format_inference_stats_dict_with_service_video_session(inference_stats_dict):

    print "Creating dictionary with inferred metric, service, video session ID and timestamp."

    dict_to_convert = {}

    for deployment in inference_stats_dict:
        if deployment == "all_deployments":
            continue
        else:
            dict_to_convert[deployment] = {
                "metrics": [],
                "timestamps": [],
                "service": [],
                "session_ids": []
            }
            for service in inference_stats_dict[deployment]:
                if service == "all_services":
                    continue
                else:
                    metric_list = []
                    timestamp_list = []
                    service_list = []
                    sessionid_list = []

                    metric_list = inference_stats_dict[deployment][service]["metrics"]
                    timestamp_list = inference_stats_dict[deployment][service]["timestamps"]
                    sessionid_list = inference_stats_dict[deployment][service]["session_ids"]
                    for entry in metric_list:
                        service_list.append(service)

                    dict_to_convert[deployment]["metrics"].extend(metric_list)
                    dict_to_convert[deployment]["timestamps"].extend(timestamp_list)
                    dict_to_convert[deployment]["service"].extend(service_list)
                    dict_to_convert[deployment]["session_ids"].extend(sessionid_list)

    return dict_to_convert

def convert_dict_to_df_with_service(dict_to_convert):

    print "Converting dictionary with metric, service and timestamp to data frame."

    final_df = pd.DataFrame()

    for deployment in dict_to_convert:
        temp_df = None
        deployment_list = []
        metrics = []
        timestamps = []
        services = []
        metrics = dict_to_convert[deployment]["metrics"]
        timestamps = dict_to_convert[deployment]["timestamps"]
        services = dict_to_convert[deployment]["service"]

        for i in range(len(metrics)):
            deployment_list.append(deployment)
        temp_df = pd.DataFrame(
            {
                "deployment": deployment_list,
                "metric": metrics,
                "timestamps": timestamps,
                "service": services
            }
        )
        final_df = final_df.append(temp_df)

    final_df = final_df.reset_index()
    final_df = final_df.drop(labels=["index"], axis=1)

    final_df = final_df.sort_values(["deployment", "timestamps"])

    dates = []

    tz = pytz.timezone("US/Eastern")

    for entry in final_df["timestamps"].values:
        # dates.append(datetime.utcfromtimestamp(int(entry)).strftime('%Y-%m-%d %H:%M:%S'))
        dates.append(datetime.fromtimestamp(int(entry), tz).strftime('%Y-%m-%d %H:%M:%S'))

    final_df["Event_date"] = dates
    final_df = final_df.drop(labels=["timestamps"], axis=1)

    return final_df

def convert_dict_to_df_with_service_video_session(dict_to_convert, target):

    print "Converting dictionary with metric, service, video session ID and timestamp to data frame."

    final_df = pd.DataFrame()

    for deployment in dict_to_convert:
        temp_df = None
        deployment_list = []
        metrics = []
        timestamps = []
        services = []
        session_ids = []
        metrics = dict_to_convert[deployment]["metrics"]
        timestamps = dict_to_convert[deployment]["timestamps"]
        services = dict_to_convert[deployment]["service"]
        session_ids = dict_to_convert[deployment]["session_ids"]

        for i in range(len(metrics)):
            deployment_list.append(deployment)
        temp_df = pd.DataFrame(
            {
                "deployment": deployment_list,
                "metric": metrics,
                "timestamps": timestamps,
                "service": services,
                "session_ids": session_ids
            }
        )
        final_df = final_df.append(temp_df)

    final_df = final_df.reset_index()
    final_df = final_df.drop(labels=["index"], axis=1)

    final_df = final_df.sort_values(["deployment", "service", "session_ids", "timestamps"])

    dates = []

    tz = pytz.timezone("US/Eastern")

    for entry in final_df["timestamps"].values:
        dates.append(datetime.fromtimestamp(int(entry), tz).strftime('%Y-%m-%d %H:%M:%S'))

    final_df["Event_date"] = dates

    # if target == "resolution":
    #     final_df = final_df.query("relative_timestamp > 60")

    final_df = final_df.drop(labels=["timestamps"], axis=1)

    return final_df

def convert_dict_to_df(dict_to_convert):

    print "Converting dictionary with metric and timestamp to data frame."

    final_df = pd.DataFrame()

    for deployment in dict_to_convert:
        temp_df = None
        deployment_list = []
        metrics = []
        timestamps = []
        metrics = dict_to_convert[deployment]["metrics"]
        timestamps = dict_to_convert[deployment]["timestamps"]
        for i in range(len(metrics)):
            deployment_list.append(deployment)
        temp_df = pd.DataFrame(
            {
                "deployment": deployment_list,
                "metric": metrics,
                "timestamps": timestamps
            }
        )
        final_df = final_df.append(temp_df)

    final_df = final_df.reset_index()
    final_df = final_df.drop(labels=["index"], axis=1)

    final_df = final_df.sort_values(["deployment", "timestamps"])

    dates = []

    tz = pytz.timezone("US/Eastern")

    for entry in final_df["timestamps"].values:
        # dates.append(datetime.utcfromtimestamp(int(entry)).strftime('%Y-%m-%d %H:%M:%S'))
        dates.append(datetime.fromtimestamp(int(entry), tz).strftime('%Y-%m-%d %H:%M:%S'))

    final_df["Event_date"] = dates
    final_df = final_df.drop(labels=["timestamps"], axis=1)

    return final_df

def export_df_to_csv(final_df, target, with_service = False):

    print "Exporting data frame with inferred metric and date in EST timezone to CSV."

    csv_path = './CSVs/'+str(target)+'/'

    if with_service:
        csv_filename = str(target) + '_with_service_stats_by_time.csv'
    else:
        csv_filename = str(target)+'_stats_by_time.csv'

    if not os.path.exists(csv_path):
        os.makedirs(csv_path)

    final_df.to_csv(csv_path + csv_filename)

    return 0

def get_most_common_resolution_per_video_session(final_df):

    print "Obtaining more common resolution per video session."

    final_df_common_res = pd.DataFrame(columns=["deployment", "metric", "service", "session_ids", "Event_date"])

    deployments_list = final_df.deployment.unique()

    deployments_array = []
    metrics_array = []
    service_array = []
    session_ids_array = []
    event_dates_array = []

    for deployment in deployments_list:
        video_sessions_ids_list = final_df.loc[final_df["deployment"] == deployment].session_ids.unique()
        for video_session in video_sessions_ids_list:
            # print "Deployment: "+deployment+", session ID: "+video_session
            # if video_session == "netflix_34:a3:95:6d:56:32_1517959025000_1517959270000":
            #     print "Pause"
            query_str = "deployment == '"+deployment+"' & session_ids == '"+video_session+"'"
            tmp_df = final_df.query(query_str)
            if tmp_df.loc[:, "metric"].mode().size > 0:
                common_res = tmp_df.loc[:, "metric"].mode()[0]
            else:
                common_res = tmp_df.iloc[0]["metric"]

            deployments_array.append(tmp_df.iloc[0]["deployment"])
            metrics_array.append(common_res)
            service_array.append(tmp_df.iloc[0]["service"])
            session_ids_array.append(tmp_df.iloc[0]["session_ids"])
            event_dates_array.append(tmp_df.iloc[0]["Event_date"])


    final_df_common_res["deployment"] = deployments_array
    final_df_common_res["metric"] = metrics_array
    final_df_common_res["service"] = service_array
    final_df_common_res["session_ids"] = session_ids_array
    final_df_common_res["Event_date"] = event_dates_array

    return final_df_common_res

def remove_first_minute_resolution(final_df):

    print "Removing the first minute for resolution"

    master_temp_df = pd.DataFrame()

    deployments = final_df["deployment"].unique()

    for deployment in deployments:

        video_sessions_ids_in_deployment = final_df.loc[final_df["deployment"] == deployment]["session_ids"].unique()

        for video_session_id in video_sessions_ids_in_deployment:
            temp_df = final_df.loc[(final_df["deployment"] == deployment) & (final_df["session_ids"] == video_session_id)]
            try:
                temp_df = temp_df[6:]
                master_temp_df = master_temp_df.append(temp_df)
            except Exception as exp:
                master_temp_df = master_temp_df.append(temp_df)
                print "Exception for "+deployment+" and "+video_session_id+": "+str(exp)

    return master_temp_df

def main():

    print "Script Start"
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--inference_dir', type=str, required=True, help="Directory where inference pickles are stored.")
    parser.add_argument('-t', '--target', type=str, required=True, default='startup', help="Inference metric, i.e. 'startup' or 'resolution'")

    args = vars(parser.parse_args())

    inference_dir = args['inference_dir']

    if inference_dir.endswith("/"):
        inference_dir = inference_dir
    else:
        inference_dir = inference_dir + "/"

    target = args['target']

    url = inference_dir + target

    # infer_stats_dict = get_target_per_deployment(url, target)
    infer_stats_dict = get_target_per_deployment_with_service_video_session(url, target)

    # dict_to_convert = format_inference_stats_dict(infer_stats_dict)
    # dict_to_convert = format_inference_stats_dict_with_service(infer_stats_dict)
    dict_to_convert = format_inference_stats_dict_with_service_video_session(infer_stats_dict)

    # final_df = convert_dict_to_df(dict_to_convert)
    # final_df = convert_dict_to_df_with_service(dict_to_convert)

    final_df = convert_dict_to_df_with_service_video_session(dict_to_convert, target)

    if target == "resolution":
        final_df = get_most_common_resolution_per_video_session(final_df)

    export_df_to_csv(final_df, target, with_service=True)
    # export_df_to_csv(final_df, target, with_service=True)

    # get_target_all_deployments(url, target)

    print "End of Script"

    return 0

if __name__ == "__main__":
  main()