#!/bin/bash
C3=$(cat c3addr)
wget $C3/openc3-google-play-reply.tar.gz -O openc3-google-play-reply.tar.gz

tar -zxvf openc3-google-play-reply.tar.gz 
docker load -i openc3-google-play-reply.img
