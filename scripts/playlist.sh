#!/bin/bash
#
# bash script to create playlist files in music subdirectories
#
# Steve Carlson (stevengcarlson@gmail.com)

find . -type d |
while read subdir
do
  rm -f "$subdir"/*.m3u
  for filename in "$subdir"/*
  do
    if [[ ${filename} =~ ^.*\.(mp3|aac|flac|loss|aif|wma)$ ]]
    then
        echo "${filename##*/}" >> ./"$subdir"/"${subdir##*/}.m3u"
    fi
  done

done