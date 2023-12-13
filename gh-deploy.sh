#!/bin/bash

mkdocs build -c -q
mkdocs gh-deploy -q
