#!/bin/bash

mkdocs build -c

git add -A
git commit -m "Update by $(date +"%Y%m%d%H%M%s")"
git push