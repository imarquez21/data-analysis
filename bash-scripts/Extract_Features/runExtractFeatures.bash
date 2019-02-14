#!/bin/bash

echo Script Start
date

echo

echo Processing Deployment 4
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-04/ -p /srv/ta_data/deployment_features_pickles > test1-04.log 2>&1 &
echo Completed Processing Deployment 4

echo

echo Processing Deployment 7
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-07/ -p /srv/ta_data/deployment_features_pickles > test1-07.log 2>&1 &
echo Completed Processing Deployment 7

echo

echo Processing Deployment 8
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-08/ -p /srv/ta_data/deployment_features_pickles > test1-08.log 2>&1 &
echo Completed Processing Deployment 4

echo

echo Processing Deployment 9
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-09/ -p /srv/ta_data/deployment_features_pickles > test1-09.log 2>&1 &
echo Completed Processing Deployment 9

echo

echo Processing Deployment 10
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-10/ -p /srv/ta_data/deployment_features_pickles > test1-10.log 2>&1 &
echo Completed Processing Deployment 10

echo

echo Processing Deployment 11
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-11/ -p /srv/ta_data/deployment_features_pickles > test1-11.log 2>&1 &
echo Completed Processing Deployment 11

echo

echo Processing Deployment 12
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-12/ -p /srv/ta_data/deployment_features_pickles > test1-12.log 2>&1 &
echo Completed Processing Deployment 12

echo

echo Processing Deployment 14
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-14/ -p /srv/ta_data/deployment_features_pickles > test1-14.log 2>&1 &
echo Completed Processing Deployment 14

echo

echo Processing Deployment 15
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-15/ -p /srv/ta_data/deployment_features_pickles > test1-15.log 2>&1 &
echo Completed Processing Deployment 15

echo

echo Processing Deployment 16
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-16/ -p /srv/ta_data/deployment_features_pickles > test1-16.log 2>&1 &
echo Completed Processing Deployment 16

echo

echo Processing Deployment sr
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-sr/ -p /srv/ta_data/deployment_features_pickles > test1-sr.log 2>&1 &
echo Completed Processing Deployment sr

echo

echo Processing Deployment tg
nohup python extract_deployment_features.py -f /srv/ta_data/deployment/test1-tg/ -p /srv/ta_data/deployment_features_pickles > test1-tg.log 2>&1 &
echo Completed Processing Deployment tg

echo

echo End of Script
date
