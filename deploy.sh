#!/bin/bash

git pull
git add -A
git commit -m "Last update by $(date +"%Y-%m-%d %H:%M:%S")"
git push