#!/bin/bash

#nohup watch -n 1200 "rsync -avzh /home/fbronzino/experiments/ta/video-ml/fin_plots/ /home/tadata/fin_plots/ &> /home/fbronzino/experiments/ta/scripts/logs/rsync2.log; chmod -R 777 /home/tadata/fin_plots/ &> /home/fbronzino/experiments/ta/scripts/logs/chmod2.log" &> /dev/null &

cmd=$!

echo $cmd

nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 0 &> logs/ml0.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 1 &> logs/ml1.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 2 &> logs/ml2.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 3 &> logs/ml3.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 4 &> logs/ml4.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 5 &> logs/ml5.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 6 &> logs/ml6.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 7 &> logs/ml7.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 8 &> logs/ml8.log &
nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 9 &> logs/ml9.log &
