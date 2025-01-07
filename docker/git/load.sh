#!/bin/bash
C3=$(cat c3addr)
wget $C3/git-client.tar.gz -O git-client.tar.gz

tar -zxvf git-client.tar.gz 
docker load -i git-client.img
