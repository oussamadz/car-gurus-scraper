#!/bin/bash

while true
do
	if pidof -x "script.py" >/dev/null; then
		echo "`pidof -x script.py`"
	else
		pkill -f firefox;
		echo "starting script on `date`";
		python3 laserapraiser.py;

	fi
	sleep 1;
done

