from google_calendar import GoogleCalendar
from trello_tasks import TrelloTasks
#what port to serve on
port = 8000

#width and height of kindle
width = 600
height = 800


def build_markdown():
    markdown = ""
    gc = GoogleCalendar()
    markdown += gc.get_events()

    tt = TrelloTasks()
    markdown += tt.get_cards('tasks', 'Doing')
    markdown += tt.get_cards('valencia','matt')

    return markdown

print(build_markdown())
