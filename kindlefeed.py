from PIL import Image, ImageDraw, ImageFont
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
fontsize = 20

#make sure this font is installed
font_path = 'FreeMono.ttf'


def make_new_squares_image():
    im = Image.new("RGB", (width,height), "white")
    draw = ImageDraw.Draw(im)

    squares = zip(
        range(0,width/2,width/2/num_squares),
        range(0,height/2,height/2/num_squares),
        range(1,255,100/num_squares))

    for x,y,colour in squares:
            coords=[x,y,width-x,height-y]
            shade = randint(0,255)
            colour=(shade,shade,shade)
            draw.rectangle(coords,fill=colour)

    font = ImageFont.truetype(font_path, fontsize)
    draw.rectangle([0,height,width,height - bottom_height],fill="white")
    text = time.ctime()
    textsize = font.getsize(text)
    draw.text([width/2-textsize[0]/2,height-bottom_height/2-textsize[1]/2],text, font=font, fill="black")
    im.save("test.png", "PNG")

def make_new_date_image():
    im = Image.new("RGB", (width,height), "white")
    draw = ImageDraw.Draw(im)
    events = getEvents.get_all()
    font = ImageFont.truetype(font_path, fontsize)
    text = events['from']
    textsize = font.getsize(text)
    line_height = textsize[1]
    l_margin = 20
    s_height = 20
    draw.text([l_margin,s_height],'Calendar:', font=font, fill="black")
    s_height += line_height
    #events
    for event in events["events"]:
        draw.text([l_margin,s_height],event['start'] + ' ' + event['summary'], font=font, fill="black")
        s_height += line_height

    draw.text([l_margin,s_height],'----', font=font, fill="black")
    s_height += line_height
    draw.text([l_margin,s_height],'Todo:', font=font, fill="black")
    s_height += line_height

    #tasks
    trello = fetch_tasks.auth()
    for task in fetch_tasks.get_tasks(trello,'To Do'):
        draw.text([l_margin,s_height],task, font=font, fill="black")
        s_height += line_height

    draw.text([l_margin,s_height],'----', font=font, fill="black")
    s_height += line_height
    draw.text([l_margin,s_height],'Doing:', font=font, fill="black")
    s_height += line_height

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
