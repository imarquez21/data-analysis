import pandas as pd
import argparse
import os
import urllib2
import json
import codecs
import numpy as np

def read_inference_folder(directory):

    final_df = pd.DataFrame()

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('.') or not file.endswith(".pickle"):
                continue
            tmp_df = pd.read_pickle(root + '/' + file)
            final_df = final_df.append(tmp_df)

    session_ids = final_df.session_id.unique()

    return session_ids

def extract_MAC_addresses(session_ids):

    mac_addresses = []

    for session_id in session_ids:
        mac = session_id.split('_')[1]
        mac_addresses.append(mac)

    tmp_set = set(mac_addresses)
    mac_addresses_list = list(tmp_set)

    return mac_addresses_list

def get_MAC_address_vendor(mac_addresses, deployment):

    # API base url,you can also use https if you need
    url = "http://macvendors.co/api/"
    vendors = []
    homes = []
    for mac_address in mac_addresses:
        try:
            request = urllib2.Request(url + mac_address, headers={'User-Agent': "API Browser"})
            response = urllib2.urlopen(request)
            # Fix: json object must be str, not 'bytes'
            reader = codecs.getreader("utf-8")
            result_json = json.load(reader(response))

            vendors.append(result_json["result"]["company"])
            homes.append(deployment)
        except Exception as exp:
            print "Exception: "+str(exp)
            print mac_address


    mac_home_df = pd.DataFrame(columns=["deployment", "mac_address", "vendor"])

    try:
        mac_home_df["deployment"] = homes
        mac_home_df["mac_address"] = mac_addresses
        mac_home_df["vendor"] = vendors
    except Exception as exp:
        print "Exception: " + str(exp)

    return mac_home_df

def main():
    print "Script Start"
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--inference_dir', type=str, required=True, help="Directory where inference pickles are stored.")
    parser.add_argument('-t', '--target', type=str, required=True,help="Target metric i.e. startup or resolution.")

    args = vars(parser.parse_args())

    directory = args['inference_dir']
    target = args['target']

    deployment_dirs = os.listdir(directory + '/' + target)

    final_mac_deployment_df = pd.DataFrame()

    for deployment in deployment_dirs:
        if deployment.startswith('.'):
            continue
        print "Processing data for home: "+deployment
        deployment_directory = directory + '/' + target + '/' + deployment
        session_ids = read_inference_folder(deployment_directory)
        mac_addresses = extract_MAC_addresses(session_ids)
        mac_deployment_df = get_MAC_address_vendor(mac_addresses, deployment)
        final_mac_deployment_df = final_mac_deployment_df.append(mac_deployment_df)

    # final_mac_deployment_df.to_csv("./CSVs/Deployment_MAC/Mac_deployment.csv")

    print "Script End"
    return 0

if __name__ == "__main__":
  main()