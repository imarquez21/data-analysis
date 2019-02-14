#!/bin/bash
echo Script Start
date
for d in /Users/ismarque/Exchange/Helium_Data/deployment_data/inference_pickles/server/startup/*/; do
	folder=$(echo $d| cut -d / -f 10)
    deployment=$(cat /home/tadata/data/controlled/video/results/"$folder"/exp.txt)
	if [[ $deployment == "test1-08" ]]; then
		echo $folder >> folders.txt
	fi
done
echo End of Script
date