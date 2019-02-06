import pandas as pd
import argparse
import datetime
import os


def save_df_to_pickle(all_common_res_df, out_dir):

    print "Saving common resolutions inference dataframe to pickle file."

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    pickle_file = "all_deployments_common_res.pickle"

    all_common_res_df.to_pickle(out_dir + "/" +pickle_file)

    return 0

def get_common_resolution(all_res_df):

    print "Obtaining common resolution per video session."

    all_common_res_df = pd.DataFrame(columns=["session_id", "common_res"])

    session_ids_array = []
    common_res_array = []

    all_res_sessions = all_res_df["session_id"]
    all_res_values = all_res_df["resolution_mc"]

    compact_all_res_df = pd.DataFrame(columns=["session_id", "resolution_mc"])
    compact_all_res_df["session_id"] = all_res_sessions
    compact_all_res_df["resolution_mc"] = all_res_values

    all_video_sessions = all_res_df.session_id.unique()

    print "Unique Video Sessions: "+str(len(all_video_sessions))

    cont = 0
    for video_session in all_video_sessions:
        query_str = "session_id == '" + video_session + "'"
        tmp_df = compact_all_res_df.query(query_str)
        if tmp_df.loc[:, "resolution_mc"].mode().size > 0:
            common_res = tmp_df.loc[:, "resolution_mc"].mode()[0]
            session_ids_array.append(video_session)
            common_res_array.append(common_res)
        else:
            common_res = tmp_df.iloc[0]["resolution_mc"]
            session_ids_array.append(video_session)
            common_res_array.append(common_res)
        cont += 1
        print "Processed "+str(cont)+"/"+str(len(all_video_sessions))+" video sessions."

    all_common_res_df["session_id"] = session_ids_array
    all_common_res_df["common_res"] = common_res_array

    return all_common_res_df

def load_all_res_pickle(pickle_file):

    print "Loading pickle with all resolution."

    all_res_df = pd.read_pickle(pickle_file)

    return all_res_df

def main():
    print "Script Start"
    print datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True, help="Pickle File with all resolution for all deployments.")
    parser.add_argument('-o', '--outdir', type=str, required=True, help="Directory where processed pickle will be saved.")

    args = vars(parser.parse_args())

    pickle = args["file"]
    outdir = args["outdir"]

    all_res_df = load_all_res_pickle(pickle)
    all_common_res_df = get_common_resolution(all_res_df)
    save_df_to_pickle(all_common_res_df, outdir)


    print "Script End"
    print datetime.datetime.now()

    return 0

if __name__ == '__main__':
    main()