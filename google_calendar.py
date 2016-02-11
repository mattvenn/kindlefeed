from __future__ import print_function
import logging
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
log = logging.getLogger('')

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

class GoogleCalendar():

    def __init__(self):
        self.get_credentials()

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)

        self.credentials = credentials

    def get_events(self, num_events=10):
        markdown = "# Calendar\n\n"
        credentials = self.credentials
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        log.info('getting the upcoming %d events' % num_events)
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=num_events, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            markdown += "No upcoming events found.\n"
            log.info("no events found")
        for event in events:
            start = event.get('start')
            if start.has_key('date'):
                start_time_str = start['date']
                start_time = datetime.datetime.strptime(start_time_str,'%Y-%m-%d')
            elif start.has_key('dateTime'):
                start_time_str = start['dateTime']
                start_time_str = event.get('start')['dateTime'].rsplit('+')[0]
                start_time = datetime.datetime.strptime(start_time_str,'%Y-%m-%dT%H:%M:%SZ')
            else:
                log.error("date issue")
                #date problem
                continue
            start_str = datetime.datetime.strftime(start_time,'%a %d %b %H:%M')
            markdown += "* %s : %s\n" % (start_str, event['summary'])

        markdown += "\n"
        return markdown


if __name__ == '__main__':
    gc = GoogleCalendar()
    print(gc.get_events())
