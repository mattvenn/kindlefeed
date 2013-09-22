from PIL import Image, ImageDraw, ImageFont
import datetime
import getEvents
import fetch_tasks
import time
from random import randint
import SocketServer
import SimpleHTTPServer
import os
#what port to serve on
port = 8000

#width and height of kindle
width = 600
height = 800
num_squares = 16
bottom_height = 100
title_fontsize = 30
fontsize = 20

#make sure this font is installed
font_path = 'FreeMono.ttf'
font = ImageFont.truetype(font_path, fontsize)
title_font = ImageFont.truetype(font_path, title_fontsize)
line_height = font.getsize('Aq')[1]
title_height = title_font.getsize('Aq')[1]


def make_new_date_image():
    im = Image.new("RGB", (width,height), "white")
    draw = ImageDraw.Draw(im)
    events = getEvents.get_all()
    font = ImageFont.truetype(font_path, fontsize)
    text = events['from']
    l_margin = 20
    s_height = 20
    draw.text([l_margin,s_height],'Calendar', font=title_font, fill="black")
    s_height += title_height
    #events
    for event in events["events"]:
        start_str = datetime.datetime.strftime(event['start'],'%a %H:%M')
        draw.text([l_margin,s_height],start_str + ' ' + event['summary'], font=font, fill="black")
        s_height += line_height

    s_height += line_height
    draw.text([l_margin,s_height],'Todo', font=title_font, fill="black")
    s_height += title_height

    #tasks
    trello = fetch_tasks.auth()
    for task in fetch_tasks.get_tasks(trello,'To Do'):
        draw.text([l_margin,s_height],task, font=font, fill="black")
        s_height += line_height

    s_height += line_height
    draw.text([l_margin,s_height],'Doing', font=title_font, fill="black")
    s_height += title_height

    for task in fetch_tasks.get_tasks(trello,'Doing'):
        draw.text([l_margin,s_height],task, font=font, fill="black")
        s_height += line_height

    im.save("test.png", "PNG")

#where we define what the server does
class getHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        #send the index.html page to the browser
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        make_new_date_image()
        image_file = open("test.png",'rb')
        image = image_file.read()
        self.wfile.write(image)

make_new_date_image()

#start the server
try:
    #this lines to allow socket reuse
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer(('',port), getHandler)
    
    print "started serving on port", port
    server.serve_forever()
except KeyboardInterrupt:
    print "quitting"
    server.socket.close()
