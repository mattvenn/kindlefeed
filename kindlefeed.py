from google_calendar import GoogleCalendar
from trello_tasks import TrelloTasks
import logging
import os

# setup logging
log = logging.getLogger('')
log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(log_format)
log.addHandler(ch)
log.setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

#what port to serve on
port = 8000

#width and height of kindle
width = 600
height = 800


def aggregate_markdown():
    markdown = ""
    gc = GoogleCalendar()
    markdown += gc.get_events()

    tt = TrelloTasks()
    markdown += tt.get_cards('tasks', 'Doing')
    markdown += tt.get_cards('valencia','matt')

    return markdown

def pandoc_to_png(markdown):
    with open('kindlefeed.md', 'w') as fh:
        fh.write(markdown)
    log.info("using pandoc to convert md -> pdf")
    os.system('pandoc --template=template.latex  kindlefeed.md -o kindlefeed.pdf')
    log.info("using imagemagick to convert pdf -> png")
    os.system('convert -alpha off -density 200 kindlefeed.pdf kindlefeed.png')


if __name__ == '__main__':
    markdown = aggregate_markdown()
    pandoc_to_png(markdown)
