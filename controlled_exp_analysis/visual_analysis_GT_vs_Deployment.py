import pandas as pd
import os
import datetime
import argparse

ta_fts_no_infocom = [
  "total_throughput_up",
  "total_throughput_down",
  "service_Video_throughput_up",
  "service_Video_throughput_down",
  "service_non_video_throughput_up",
  "service_non_video_throughput_down",
  "parallel_flows",
  'userPacketCount',
  'serverPacketCount',
  'userByteCount',
  'serverByteCount',
]

gt_ta_fts_no_infocom = [
  "total_throughput_up",
  "total_throughput_down",
  "service_Video_throughput_up",
  "service_Video_throughput_down",
  "service_non_video_throughput_up",
  "service_non_video_throughput_down",
  "parallel_flows",
  # 'userPacketCount',
  # 'serverPacketCount',
  # 'userByteCount',
  # 'serverByteCount',
]

chunk_fts = [
  "chunk_start_time",
  "chunk_end_time",
  "10_EWMA_chunksizes",
  "10_std_chunksize",
  "10_avg_chunksize",
  "10_max_chunksize",
  "10_min_chunksize",
  "10_chunksizes_50",
  "10_chunksizes_75",
  "10_chunksizes_85",
  "10_chunksizes_90",
  "allprev_std_chunksize",
  "allprev_avg_chunksize",
  "allprev_max_chunksize",
  "allprev_min_chunksize",
  "allprev_chunksizes_50",
  "allprev_chunksizes_75",
  "allprev_chunksizes_85",
  "allprev_chunksizes_90",
  "cumsum_chunksizes",
  "curr_chunksize",
  "size_diff_previous",
  "all_prev_up_chunk_iat_avg",
  "all_prev_up_chunk_iat_std",
  "all_prev_up_chunk_iat_min",
  "all_prev_up_chunk_iat_max",
  "all_prev_up_chunk_iat_50",
  "all_prev_up_chunk_iat_75",
  "all_prev_up_chunk_iat_85",
  "all_prev_up_chunk_iat_90",
  "all_prev_down_chunk_iat_avg",
  "all_prev_down_chunk_iat_std",
  "all_prev_down_chunk_iat_min",
  "all_prev_down_chunk_iat_max",
  "all_prev_down_chunk_iat_50",
  "all_prev_down_chunk_iat_75",
  "all_prev_down_chunk_iat_85",
  "all_prev_down_chunk_iat_90",
  'up_chunk_iat_avg',
  'up_chunk_iat_std',
  'up_chunk_iat_min',
  'up_chunk_iat_max',
  'up_chunk_iat_50',
  'up_chunk_iat_75',
  'up_chunk_iat_85',
  'up_chunk_iat_90',
  'down_chunk_iat_avg',
  'down_chunk_iat_std',
  'down_chunk_iat_min',
  'down_chunk_iat_max',
  'down_chunk_iat_50',
  'down_chunk_iat_75',
  'down_chunk_iat_85',
  'down_chunk_iat_90',
  "current_chunk_iat",
  "up_down_ratio",
  "n_prev_up_chunk",
  "n_prev_down_chunk",
  "n_chunks_down", #number of chunks down in time slot
  "n_chunks_up",  #number of chunks up in time slot
]

features = ta_fts_no_infocom + chunk_fts
features_gt = gt_ta_fts_no_infocom + chunk_fts

def save_pickle_and_csv(df_gt, df_deployment, out_dir):

    print "Saving DFs to pickle and CSV."

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # df_gt.to_pickle(out_dir + "/GT_features.pickle")
    df_gt.to_csv(out_dir + "/GT_features.csv")
    # df_deployment.to_pickle(out_dir + "/Deployment_features.pickle")
    df_deployment.to_csv(out_dir + "/Deployment_features.csv")

    return 0


def select_columns(df_gt, df_deployment, target, out_dir):

    print "Selecting colunmns to make comparisson."

    stt_gt = ["startup_time", "absolute_timestamp"]
    res_gt = ["resolution", "absolute_timestamp"]

    stt_inf = ["startup_mc", "absolute_timestamp"]
    res_inf = ["resolution_mc", "absolute_timestamp"]

    if target == 's':
        gt_columns = features_gt + stt_gt
        deployment_columns = features + stt_inf
    else:
        gt_columns = features_gt + res_gt
        deployment_columns = features + res_inf

    new_df_gt = df_gt[gt_columns]
    new_df_deployment = df_deployment[deployment_columns]

    save_pickle_and_csv(new_df_gt, new_df_deployment, out_dir)

    return 0

def main():

    print "Script Start."
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()

    parser.add_argument('-g', '--gt', type=str, required=True, help="Pickle file with GT values")
    parser.add_argument('-d', '--deployment', type=str, required=True,
                        help="Pickle file with inference values based on .out files, aka deployment data.")

    parser.add_argument('-o', '--outdir', type=str, required=True, help="Directory to save the files after being processed.")
    parser.add_argument('-t', '--target', type=str, required=True,
                        help="Resolution [r], or Startup [s]")

    args = vars(parser.parse_args())

    gt = args["gt"]
    deployment = args["deployment"]
    out_dir = args["outdir"]
    target = args["target"]

    print "Loading pickles as Dataframes."

    gt_df = pd.read_pickle(gt)
    deployment_df = pd.read_pickle(deployment)

    select_columns(gt_df, deployment_df, target, out_dir)


    print "Script End."
    print datetime.datetime.now()

    return 0


if __name__ == '__main__':
    main()