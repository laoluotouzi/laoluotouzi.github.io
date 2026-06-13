#!/bin/bash
# 构建博客并启动本地预览服务

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=8080

echo ">>> 构建博客..."
python3.11 "$SCRIPT_DIR/src/generator.py" build || exit 1

PID=$(lsof -ti:$PORT 2>/dev/null)
if [ -n "$PID" ]; then
    echo ">>> 端口 $PORT 被占用 (PID: $PID)，正在终止..."
    kill -9 $PID 2>/dev/null
    sleep 1
fi

echo ">>> 启动预览服务: http://localhost:$PORT"
python3.11 -m http.server $PORT --directory "$SCRIPT_DIR/dist"
