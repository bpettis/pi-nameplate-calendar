#!/bin/bash
# If you want the calendar updates to happen on a schedule, set a cronjob to run *this* script
# rather than the python script itself. This is my clunky way of ensuring that we're 
# invoking the script from the correct working directory so that the correct .env file
# is loaded and all that other fun stuff.

source /home/bpettis/nameplate/.venv/bin/activate
cd /home/bpettis/nameplate
/home/bpettis/nameplate/.venv/bin/python3 download_calendar.py
