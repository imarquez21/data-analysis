#!/bin/bash
echo Script Start
date
echo $1
echo $2
echo Logic Test Now
if [[ $1 == "test1-08" ]]; then
	echo $2
fi
echo Script End
date