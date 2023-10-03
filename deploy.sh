#!/bin/bash

git pull
git add -A
git commit -m "Last update time: $(date +"%Y-%m-%d %H:%M:%S")"
git push
