#!/bin/bash

echo Script Start
date

echo

echo Processing Deployment 1
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-01 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-01.log
echo Completed Processing Deployment 1

echo


echo

echo Processing Deployment 2
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-02 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-02.log
echo Completed Processing Deployment 2

echo

echo

echo Processing Deployment 3
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-03 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-03.log
echo Completed Processing Deployment 3

echo

echo

echo Processing Deployment 4
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-04 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-04.log
echo Completed Processing Deployment 4

echo

echo

echo Processing Deployment 4
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-04 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-04.log
echo Completed Processing Deployment 4

echo

echo Processing Deployment 7
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-07 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-07.log
echo Completed Processing Deployment 7

echo

echo Processing Deployment 8
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-08 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-08.log
echo Completed Processing Deployment 4

echo

echo Processing Deployment 9
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-09 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-09.log
echo Completed Processing Deployment 9

echo

echo Processing Deployment 10
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-10 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-10.log
echo Completed Processing Deployment 10

echo

echo Processing Deployment 11
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-11 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-11.log
echo Completed Processing Deployment 11

echo

echo Processing Deployment 12
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-12 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-12.log
echo Completed Processing Deployment 12

echo

echo Processing Deployment 14
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-14 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-14.log
echo Completed Processing Deployment 14

echo

echo Processing Deployment 15
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-15 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-15.log
echo Completed Processing Deployment 15

echo

echo Processing Deployment 16
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-16 -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-16.log
echo Completed Processing Deployment 16

echo

echo Processing Deployment sr
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-sr -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-sr.log
echo Completed Processing Deployment sr

echo

echo Processing Deployment tg
python extract_deployment_features.py -f /srv/ta_data/deployment/test1-tg -p /srv/ta_data/deployment_features_pickles/00_TraceRoute > Log_files/test1-tg.log
echo Completed Processing Deployment tg

echo

echo End of Script
date
