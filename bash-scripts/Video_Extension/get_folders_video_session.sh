#!/bin/bash
echo Script Start
date
for d in /Users/ismarque/Exchange/Helium_Data/deployment_data/inference_pickles/server/startup/*/; do
	deployment=$(echo $d| cut -d / -f 10)
    echo Linebreak
    echo Processing $deployment
    echo cat /home/tadata/data/controlled/video/results/"$deployment"/exp.txt >> folders.txt
    echo Linebreak
done
echo End of Script
date