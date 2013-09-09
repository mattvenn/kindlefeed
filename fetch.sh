#!/bin/sh
#put this in /mnt/us/fetch.sh and make executable
#add cronjob to run it whenever

file="/tmp/test.png"
rm $file
wget "http://192.168.0.12:8000/" -O $file
if [ -e $file ]; then
	echo "got file"
	mv $file /mnt/us/linkss/screensavers/
fi
