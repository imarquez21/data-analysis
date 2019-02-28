import pandas as pd
import argparse
import datetime
import pyprind
import os

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

res_gt = ["resolution", "absolute_timestamp", "session_id"]
res_inf = ["resolution_mc", "absolute_timestamp", "session_id"]

features = ta_fts_no_infocom + chunk_fts
features_gt = gt_ta_fts_no_infocom + chunk_fts

def save_pickle(inference_df, out_dir, file_name):

    print "Saving " + file_name + " inference pickle."

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


    inference_df.to_pickle(out_dir + "/" +file_name + ".pickle")
    inference_df.to_csv(out_dir + "/" + file_name + ".csv")

    return 0

def get_common_res(df, gt):


    if gt:
        column_tag = "resolution"
        print "Obtaining common resolution per video session for GT."
    else:
        column_tag = "resolution_mc"
        print "Obtaining common resolution per video session for deployment inference."

    df.reset_index(inplace=True)

    all_common_res_df = pd.DataFrame(columns=["absolute_timestamp", "session_id", "common_res"])

    session_ids_array = []
    common_res_array = []
    abs_timestamps_array = []



    all_res_sessions = df["session_id"]
    all_res_values = df[column_tag]
    all_ts_values = df["absolute_timestamp"]

    compact_all_res_df = pd.DataFrame(columns=["session_id", "resolutions", "absolute_timestamp"])
    compact_all_res_df["session_id"] = all_res_sessions
    compact_all_res_df["resolutions"] = all_res_values
    compact_all_res_df["absolute_timestamp"] = all_ts_values

    all_video_sessions = df.session_id.unique()

    print "Unique Video Sessions: " + str(len(all_video_sessions))
    bar = pyprind.ProgBar(len(all_video_sessions), monitor=True, title="Get Common Resolution")

    # cont = 0
    for video_session in all_video_sessions:
        query_str = "session_id == '" + video_session + "'"
        tmp_df = compact_all_res_df.query(query_str)
        if tmp_df.loc[:, "resolutions"].mode().size > 0:
            common_res = tmp_df.loc[:, "resolutions"].mode()[0]
            session_ids_array.append(video_session)
            common_res_array.append(common_res)
            abs_timestamps_array.append(tmp_df.iloc[0]["absolute_timestamp"])
        else:
            common_res = tmp_df.iloc[0]["resolutions"]
            session_ids_array.append(video_session)
            common_res_array.append(common_res)
            abs_timestamps_array.append(tmp_df.iloc[0]["absolute_timestamp"])
        # cont += 1
        # print "Processed "+str(cont)+"/"+str(len(all_video_sessions))+" video sessions."
        bar.update()

    print bar
    all_common_res_df["absolute_timestamp"] = abs_timestamps_array
    all_common_res_df["session_id"] = session_ids_array
    all_common_res_df["common_res"] = common_res_array

    return all_common_res_df


    return 0

def compare_res(gt_df, inference_df):

    # Sort ascending both data frames based on the absolute timestamp
    gt_df.sort_values("absolute_timestamp", inplace=True)
    inference_df.sort_values("absolute_timestamp", inplace=True)

    # From GT get the first and last timestamp in the dataframe.
    start_ts = gt_df.iloc[0]["absolute_timestamp"]
    end_ts = gt_df.iloc[-1]["absolute_timestamp"]

    # Set absolute timestamp as the index in order to apply index.get_loc later on.
    gt_df.set_index("absolute_timestamp", inplace=True)
    inference_df.set_index("absolute_timestamp", inplace=True)

    # Remove the rows with duplicated index.
    inference_df = inference_df[~inference_df.index.duplicated(keep='first')]

    startloc = inference_df.index.get_loc(start_ts, method="nearest")
    endloc = inference_df.index.get_loc(end_ts, method="nearest")

    slice_inference_df = inference_df.iloc[startloc:endloc]

    gt_columns = features_gt + res_gt
    deployment_columns = features + res_inf

    gt_common_res_df = get_common_res(gt_df, gt=True)
    inference_common_res_df = get_common_res(slice_inference_df, gt=False)

    gt_df = gt_df[gt_columns]
    slice_inference_df = slice_inference_df[deployment_columns]

    save_pickle(gt_df, "./Pickles_and_CSVs", "GT_dataframe")
    save_pickle(slice_inference_df, "./Pickles_and_CSVs", "Inference_Slice")
    save_pickle(gt_common_res_df, "./Pickles_and_CSVs", "GT_Common_Res")
    save_pickle(inference_common_res_df, "./Pickles_and_CSVs", "Inference_Common_Res")

    return 0

def load_model(gt_pickle, inference_pickle):

    gt_df = pd.read_pickle(gt_pickle)
    inference_df = pd.read_pickle(inference_pickle)

    # print "Pause"

    compare_res(gt_df, inference_df)
    return gt_df, inference_df

def main():

    print "Script start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gt', type=str, required=True, help="Pickle file associated to GT.")
    parser.add_argument('-d', '--deployment', type=str, required=True, help="Pickle file associated to inference based on deployment data.")

    args = vars(parser.parse_args())

    load_model(args["gt"], args["deployment"])

    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()