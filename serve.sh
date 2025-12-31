#!/bin/bash

PORT=8000

echo "正在检查端口 $PORT 是否被占用..."

# 方法1: 使用 lsof (macOS, Linux常用)
PID=$(lsof -ti:$PORT 2>/dev/null)

# 如果方法1失败，尝试方法2: 使用 ss (部分Linux系统)
if [ -z "$PID" ]; then
    PID=$(ss -tlnp | grep ":$PORT " | awk '{print $NF}' | cut -d',' -f2 | cut -d'=' -f2)
fi

if [ ! -z "$PID" ]; then
    echo "端口 $PORT 被进程 $PID 占用。"
    # 终止进程
    kill -9 $PID 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "已终止进程。"
        # 可选：等待端口释放
        sleep 1
    else
        echo "警告：无法终止进程 $PID。可能会启动失败。" >&2
    fi
else
    echo "端口 $PORT 未被占用。"
fi

echo "正在启动 mkdocs serve..."

mkdocs serve -a 127.0.0.1:$PORT