#!/bin/bash

reviewId=$(openssl rand -hex 8)

data="{\"reviewId\": \"$reviewId\", \"text\": \"Hello, World!\"}"

curl -X POST -H "Content-Type: application/json" -d "$data" http://localhost:8080/

