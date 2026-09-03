#!/bin/bash

# Set this script to run on boot - this will launch the button listener
# which should be running all the time for us to manually trigger the
# other scripts via button presses

source /home/bpettis/nameplate/.venv/bin/activate
cd /home/bpettis/nameplate
sudo -E env PATH=$PATH /home/bpettis/nameplate/.venv/bin/python3 button_listener.py
