#!/bin/bash

NAME=$1

if [ "X$NAME" == "X" ];then
    echo $0 NAME
    exit 1
fi

docker stop openc3-google-play-reply-$NAME 2>/dev/null
docker rm openc3-google-play-reply-$NAME 2>/dev/null

PORT=$(cat conf/$NAME/config.yaml |grep ^port:|awk '{print $2}' )
PROXY=$(cat conf/$NAME/config.yaml|grep ^proxy:|awk '{print $2}'|sed  "s/'//g")

http_proxy="-e http_proxy=$PROXY"
https_proxy="-e https_proxy=$PROXY"
echo "PROXY: [$PROXY]"

if [ -z "$PROXY" ]; then
    echo "Error: proxy not found in the config"
    exit 1
fi

if [ $PROXY = "null" ]; then
    http_proxy=""
    https_proxy=""
fi
docker run -it -d \
  --name openc3-google-play-reply-$NAME \
   -v ./code:/code \
   -v ./conf/$NAME:/conf \
   -v ./config.yaml:/config.yaml \
   -p $PORT:8080 \
   -e app_package_name=$NAME \
   $http_proxy \
   $https_proxy \
   openc3-google-play-reply
