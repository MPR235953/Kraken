#!/bin/bash
cron
python ./data_loader.py
tail -f /dev/null