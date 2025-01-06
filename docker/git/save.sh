#!/bin/bash

docker save -o git-client.img git-client:latest
tar -zcvf git-client.tar.gz git-client.img 
rm -f git-client.img
mv git-client.tar.gz /data/open-c3/c3-front/dist/
