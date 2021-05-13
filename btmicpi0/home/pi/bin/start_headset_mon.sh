#!/bin/bash
if [ -n "`ps -fC python3 | grep headset_mon.py`" ]; then exit; fi
/home/pi/bin/headset_mon.py &
