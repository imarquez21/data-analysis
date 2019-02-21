#!/bin/bash

#echo 'sudo chmod -R 777 /home/tadata/data/controlled/'

#sudo chmod -R 777 /home/tadata/data/controlled/

echo 'python /home/ismarque/experiments/ta/video-ml/featureExtraction/process_pickles_traffic.py'

#python /home/fbronzino/experiments/ta/video-ml/featureExtraction/process_pickles_traffic.py -f /home/tadata/data/controlled/video/results/ -r &> /home/fbronzino/experiments/ta/scripts/logs/aggr2.log
python /home/ismarque/experiments/ta/video-ml/featureExtraction/process_pickles_traffic.py -f /home/tadata/data/controlled/video/results/ -r &> /home/ismarque/experiments/logs/aggr2.log

echo 'cp /home/tadata/data/controlled/video/results/*.pkl /home/ismarque/experiments/ta/video-ml/data/'

cp /home/tadata/data/controlled/video/results/*.pkl /home/ismarque/experiments/ta/video-ml/data/

/home/ismarque/experiments/ta/scripts/do_ml_selected.sh
