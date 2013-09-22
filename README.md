# google calendar on kindle screensaver

based on a lot of posts from hackaday, particularly this one: http://hackaday.com/2013/08/28/kindle-hack-ads-value-to-the-wallpaper/

now with trello todo lists

# requirements

A kindle and a server.

# todo

We should generate the doc with html and then convert?

## kindle

see above link for these:

* jail broken kindle
* screen saver hack 

then install the fetch.sh to /mnt/us/fetch.sh, make executable and make a crontab to run it now and then. You'll also need to edit fetch.sh to use the correct ip/address of your server.

## server

on the server you'll need PIL with truetype enabled and the google api stuff.

### PIL

* apt-get install libfreetype6-dev
* apt-get install python-imaging

### Google api & oauth2

* sudo pip install --upgrade google-api-python-client

First go to google's api console: https://code.google.com/apis/console and create a new project with calendar access enabled. Copy your id and secret to a new file called client.py:

    client_id='xxx'
    client_secret='xxx'

Then edit getEvents.py. In auth() you'll have to first uncomment the part that gives you the redirect url, fetch a code and then uncomment the next part to turn the code into a token that is stored locally. Recomment the parts after use!

If that works, then when you run getEvents.py it will return you your events for the next 7 days.

### trello

Install with pip install py-trello

First get an api key from trello: https://trello.com/1/appKey/generate

I couldn't get oauth to work properly, so only using the api key and the oauth token. Get the oauth token with the oauth_util.py

Keys have to be put in trellokeys.py

# kindlefeed.py

Now run the kindlefeed.py, it will first render test.png with your events in it. Then it starts listening on port 8000 and when you make a request will render the events as a kindle sized png.
