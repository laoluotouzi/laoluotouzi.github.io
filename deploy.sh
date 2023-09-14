#!/bin/bash

mkdocs build -c

git add -A
git commit -m "Update by $(date)"
git push