#!/bin/bash

NAME=$1

if [ "X$NAME" == "X" ];then
    echo $0 NAME
    exit 1
fi

docker exec -it -w /code google-play-reply-$NAME bash -c "pip install -r requirements.txt"
