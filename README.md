# google calendar & trello tasks on kindle screensaver

based on a lot of posts from hackaday, particularly this one: http://hackaday.com/2013/08/28/kindle-hack-ads-value-to-the-wallpaper/

now with trello todo lists

# requirements

A kindle and a server (raspberry pi, or your laptop will work too).

## kindle

see above link for these:

* jail broken kindle
* screen saver hack 

then install the fetch.sh to /etc/network/if-up.d/fetch
and make executable. You'll also need to edit fetch.sh to use the correct ip/address of your server.

## server

install requirements with pip -r python-requirements.txt

### calendar

follow [these
instructions](https://developers.google.com/google-apps/calendar/quickstart/python)
to get your oauth setup.

Running python google_calendar.py should print out your next 5 events.

### trello

Install with pip install py-trello

First get an api key from trello: https://trello.com/1/appKey/generate

I couldn't get oauth to work properly, so only using the api key and the oauth token. Get the oauth token with the oauth_util.py

Keys have to be put in trellokeys.py

# kindlefeed.py

    sudo cp kindlefeed.conf /etc/supervisor/conf.d
    sudo supervisorctl reread
    sudo supervisorctl update

It starts listening on port 8000 and when you make a request will render the events as a kindle sized png.
