#!/bin/sh
#put this in /etc/network/if-up.d/fetch and make executable
#use mntroot rw to make filesystem writeable
#then mntroot ro
date >> /tmp/lastfetch
file="/tmp/test.png"
rm -f $file
wget "http://192.168.1.206:8000/kindlefeed.png" -O $file
if [ -e $file ]; then
        echo "got file"
        mv $file /mnt/us/linkss/screensavers/
fi
