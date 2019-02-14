#!/bin/bash

echo Script Start
date

echo Processing Deployment test1-01
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-01 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-01.log
echo Completed Deployment test1-01

echo Processing Deployment test1-05
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-05 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-05.log
echo Completed Deployment test1-05

echo Processing Deployment test1-06
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-06 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-06.log
echo Completed Deployment test1-06

echo Processing Deployment test1-07
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-07 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-07.log
echo Completed Deployment test1-07

echo Processing Deployment test1-08
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-08 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-08.log
echo Completed Deployment test1-08

echo Processing Deployment test1-12
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-12 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-12.log
echo Completed Deployment test1-12

echo Processing Deployment test1-14
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-14 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-14.log
echo Completed Deployment test1-14

echo Processing Deployment test1-15
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-15 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-15.log
echo Completed Deployment test1-15

echo Processing Deployment test1-16
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-16 -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-16.log
echo Completed Deployment test1-16

echo Processing Deployment test1-sr
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-sr -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-sr.log
echo Completed Deployment test1-sr

echo Processing Deployment test1-tg
python predict_regression.py -f /srv/ta_data/deployment_features_pickles/access_wireless_traceroute/test1-tg -p /srv/ta_data/inference_pickles/access_wireless_traceroute -t resolution > ./Log_files_resolution/test1-tg.log
echo Completed Deployment test1-tg


echo Script End
date
