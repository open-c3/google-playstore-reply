#!/bin/bash

SOCK=$(cat socks)
docker run -it \
   -v /data/google-playstore-reply:/code \
   -v /root/.ssh:/root/.ssh \
   -e http_proxy=socks5://$SOCK \
   -e https_proxy=socks5://$SOCK \
   git-client git push
