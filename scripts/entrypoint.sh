#!/bin/bash
set -e

/usr/bin/python3 tools/app.py &> /var/log/tools.log &
tail -Fq /var/log/tools.log /var/log/verbose-tools.log
