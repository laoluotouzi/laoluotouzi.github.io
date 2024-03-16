#!/bin/bash

find ./docs/attachments -name "*.png" -type f -exec chmod 644 {} +
find ./docs/attachments -name "*.jpg" -type f -exec chmod 644 {} +
find ./docs/attachments -name "*.jpeg" -type f -exec chmod 644 {} +