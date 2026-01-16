#!/usr/bin/env bash
python3 src/main.py
#Creating local web server
cd public && python3 -m http.server 8888