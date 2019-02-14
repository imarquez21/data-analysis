#!/bin/bash
echo Script Start
date
mkdir -p ./$1;
for d in /home/tadata/data/controlled/video/results/*/; do
	folder=$(echo $d| cut -d / -f 8)
    	deployment=$(cat /home/tadata/data/controlled/video/results/"$folder"/exp.txt)
	#echo $folder >> log.txt
	#echo $deployment >> log.txt
	if [[ $deployment == "$1"* ]]; then
		if [[ $deployment == *"amazon"* ]]; then
			mkdir -p ./$1/amazon/$folder
			cp /home/tadata/data/controlled/video/results/"$folder"/session_time_10.pkl ./$1/amazon/$folder
		fi
		if [[ $deployment == *"netflix"* ]]; then
			mkdir -p ./$1/twitch/$folder
			cp /home/tadata/data/controlled/video/results/"$folder"/session_time_10.pkl ./$1/netflix/$folder
		fi
		if [[ $deployment == *"twitch"* ]]; then
			mkdir -p ./$1/twitch/$folder
			cp /home/tadata/data/controlled/video/results/"$folder"/session_time_10.pkl ./$1/twitch/$folder
		fi
		if [[ $deployment == *"youtube"* ]]; then
			mkdir -p ./$1/youtube/$folder
			cp /home/tadata/data/controlled/video/results/"$youtube"/session_time_10.pkl ./$1/youtube/$folder
		fi
	fi
done
echo End of Script
date