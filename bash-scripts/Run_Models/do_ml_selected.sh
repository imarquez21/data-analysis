#!/bin/bash

#nohup watch -n 1200 "rsync -avzh /home/fbronzino/experiments/ta/video-ml/fin_plots/ /home/tadata/fin_plots/ &> /home/fbronzino/experiments/ta/scripts/logs/rsync2.log; chmod -R 777 /home/tadata/fin_plots/ &> /home/fbronzino/experiments/ta/scripts/logs/chmod2.log" &> /dev/null &

cmd=$!

echo $cmd

#nohup python /home/fbronzino/experiments/ta/video-ml/all_tests.py 4 &> /home/ismarque/experiments/logs/ml4.log &
nohup python /home/ismarque/experiments/ta/video-ml/all_tests.py 4 &> /home/ismarque/experiments/logs/ml4.log &
