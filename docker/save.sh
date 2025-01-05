#!/bin/bash
docker save -o openc3-google-play-reply.img openc3-google-play-reply:latest
tar -czvf openc3-google-play-reply.tar.gz openc3-google-play-reply.img
rm -f openc3-google-play-reply.img
mv openc3-google-play-reply.tar.gz /data/open-c3/c3-front/dist/
