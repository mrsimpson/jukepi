#!/bin/bash
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for filename in $(ls)
    do
    REGEX="^(.*)[[:space:]]-[[:space:]](.*)[[:space:]]-[[:space:]](.*)$"
    if [[ ${filename} =~ ${REGEX} ]]; then
        ARTIST=${BASH_REMATCH[1]}
        ALBUM=${BASH_REMATCH[2]}
        INDEX=${BASH_REMATCH[3]}
        if [ ! -d "${ARTIST}" ]; then
            mkdir ${ARTIST}
        fi
        if [ ! -d "${ARTIST}/$ALBUM" ]; then
            mkdir ${ARTIST}/$ALBUM
        fi
        mv ${filename} ${ARTIST}/${ALBUM}
    fi
    done

IFS=$SAVEIFS