#!/bin/bash

NAME=$1

if [ "X$NAME" == "X" ];then
    echo $0 NAME
    exit 1
fi

docker run -it -d --name openc3-google-play-reply-$NAME -v ./code:/code -v ./conf/$NAME:/conf openc3-google-play-reply
