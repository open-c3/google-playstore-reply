#!/bin/bash

TEMP_FILE="/tmp/process_pids.txt"
PROCESSES=("/task.py" "/list.py")

# 函数：获取进程 PID（可能有多个）
get_pids_by_name() {
    pgrep -f "$1"
}

# 函数：终止进程
kill_process() {
    local pid=$1
    local process_name=$2
    if ps -p $pid > /dev/null 2>&1; then
        if ps -p $pid -f | grep -q "$process_name"; then
            kill -9 $pid
            echo "Killed process $process_name with PID $pid"
        else
            echo "Process with PID $pid is not $process_name"
        fi
    else
        echo "Process with PID $pid does not exist"
    fi
}

# 读取并终止之前记录的进程
if [ -f "$TEMP_FILE" ]; then
    while IFS=: read -r process pid; do
        kill_process "$pid" "$process"
    done < "$TEMP_FILE"
fi

# 清空临时文件
> "$TEMP_FILE"

# 查找并记录新的进程 PID
for process in "${PROCESSES[@]}"; do
    pids=$(get_pids_by_name "$process")
    if [ ! -z "$pids" ]; then
        for pid in $pids; do
            echo "$process:$pid"  ##
            echo "$process:$pid" >> "$TEMP_FILE"
            echo "Found $process with PID $pid"
        done
    fi
done

