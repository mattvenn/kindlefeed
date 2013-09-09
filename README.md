# google calendar on kindle screensaver

based on a lot of posts from hackaday, particularly this one: 

    http://hackaday.com/2013/08/28/kindle-hack-ads-value-to-the-wallpaper/

# requirements

## kindle

see above link for these:

* jail broken kindle
* screen saver hack 

then install the fetch.sh to /mnt/us/fetch.sh, make executable and make a crontab to run it now and then.

## server

on the server you'll need PIL with truetype enabled and the google api stuff.

### PIL

* apt-get install libfreetype6-dev
* apt-get install python-imaging

### Google api

* sudo pip install --upgrade google-api-python-client

You'll have to first create a client.py file with your id and secret in it. These come from the google api manager.

Then look at getEvents.py, in auth() you'll have to first uncomment the part that gives you the redirect url, fetch a code and then uncomment the next part to turn the code into a token that is stored locally. 

If that works, then when you run getEvents.py it will return you your events for the next 7 days.

# kindlefeed.py

Then run the kindlefeed.py, it will start listening on port 8000 and when you make a request will render the events as a kindle sized png.
