#!/bin/bash

echo Script Start
date

python extract_deployment_features.py -f /srv/ta_data/deployment/test1-01 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-01.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-02 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-02.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-03 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-03.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-04 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-04.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-05 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-05.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-06 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-06.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-07 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-07.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-08 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-08.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-09 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-09.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-10 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-10.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-11 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-11.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-12 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-12.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-14 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-14.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-15 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-15.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-16 -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-16.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-sr -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-sr.log
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-tg -p /srv/ta_data/deployment_features_pickles/all_access_wireless_traceroute > Log_files/test1-tg.log

echo Script End
date
