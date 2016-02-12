#!/usr/bin/env python
import datetime
import SimpleHTTPServer, SocketServer
from google_calendar import GoogleCalendar
from trello_tasks import TrelloTasks
import logging
import os

#what port to serve on
port = 8000

# setup logging
log = logging.getLogger('')
log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(log_format)
log.addHandler(ch)
log.setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)


def aggregate_markdown():
    markdown = ""
    gc = GoogleCalendar()
    markdown += gc.get_events()

    tt = TrelloTasks()
    markdown += tt.get_cards('tasks', 'Doing')
    markdown += tt.get_cards('valencia','matt')

    now = datetime.datetime.now()
    update_str = datetime.datetime.strftime(now,'### Updated %d/%m at %H:%M')
    markdown += update_str

    return markdown

def pandoc_to_png(markdown):
    with open('kindlefeed.md', 'w') as fh:
        fh.write(markdown)
    log.info("using pandoc to convert md -> pdf")
    os.system('pandoc --template=template.latex  kindlefeed.md -o kindlefeed.pdf')
    log.info("using imagemagick to convert pdf -> png")
    os.system('convert -alpha off -density 200 kindlefeed.pdf kindlefeed.png')


#where we define what the server does
class getHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        #send the index.html page to the browser
        log.info("got request")
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()

        markdown = aggregate_markdown()
        pandoc_to_png(markdown)

        image_file = open("kindlefeed.png")
        image = image_file.read()
        self.wfile.write(image)
        log.info("done")


if __name__ == '__main__':
    #start the server
    try:
        #this lines to allow socket reuse
        SocketServer.TCPServer.allow_reuse_address = True
        server = SocketServer.TCPServer(('',port), getHandler)
        
        logging.info("started serving on port %d" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("caught ^C - quitting")
    server.socket.close()
