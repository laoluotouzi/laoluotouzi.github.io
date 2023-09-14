#!/bin/bash

date_time=$(date)

mkdocs build -c

git add -A
git commit -m "Update by $(date_time)"
git push