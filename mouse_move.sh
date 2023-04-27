#!/bin/bash

while :
do
	xdotool mousemove 0 0  click 1 mousemove restore
	sleep 60
	if ps -p "$1" > /dev/null;
	then
		echo "running"
	else
		echo "not running"
		break
	fi
done