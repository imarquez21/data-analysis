#!/bin/bash

filename="exp.txt"

for DIR in ./*/
do
    echo $DIR$filename
    #sed -i '' 's/test1-08/lab10/g' $DIR$filename
    cat $DIR$filename
done

