#!/bin/env bash

echo sync ...

if [ ! -f "/conf/on" ]; then
    echo "File /conf/on does not exist, exiting..."
    exit 0
fi

/code/task.py /code/prod/list.py
