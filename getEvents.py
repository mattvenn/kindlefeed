from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build
import datetime;
import httplib2
import client

SCOPES = [ 'https://www.google.com/calendar/feeds/']  
USER_AGENT = ''

def auth():
    flow = OAuth2WebServerFlow(client_id=client.client_id,
                               client_secret=client.client_secret,
                               scope=SCOPES,
                               redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    #first uncomment these lines, and go to the link in your browser
    #auth_uri = flow.step1_get_authorize_url()
    #print auth_uri

    #copy the code you get below, and use it to get and then store the credentials
    #code = ''
    #credentials = flow.step2_exchange(code)
    #then store the creds
    #storage.put(credentials)

    storage = Storage('a_credentials_file')
    credentials = storage.get()
    return credentials

def fetch(credentials,calendar_id):
    #print credentials
    ret = {}

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('calendar', 'v3', http=http)
    now = datetime.datetime.now()
    then = now + datetime.timedelta(days=7)
    from_time = datetime.datetime.strftime(now,'%Y-%m-%dT%H:%M:%S+00:00')
    to_time = datetime.datetime.strftime(then,'%Y-%m-%dT%H:%M:%S+00:00')
    ret['from'] = 'from:' + datetime.datetime.strftime(now,'%d/%m/%Y')
    ret['to'] = 'to:' + datetime.datetime.strftime(then,'%d/%m/%Y')
    ret['events'] = []

    #make the request
	
    request = service.events().list(calendarId=calendar_id,timeMax=to_time,timeMin=from_time,singleEvents=True,maxResults=10,orderBy='startTime')
    #request = service.events().list(calendarId='primary',timeMax=to_time,timeMin=from_time,singleEvents=True,maxResults=10,orderBy='startTime')
    response = request.execute()
    for event in response.get('items', []):
        #chuck timezone
        start = event.get('start')
        if start.has_key('date'):
            start_time_str = start['date']
            start_time = datetime.datetime.strptime(start_time_str,'%Y-%m-%d')
        elif start.has_key('dateTime'):
            start_time_str = start['dateTime']
            start_time_str = event.get('start')['dateTime'].rsplit('+')[0]
            start_time = datetime.datetime.strptime(start_time_str,'%Y-%m-%dT%H:%M:%S')
        else:
            #date problem
            continue
        #print start_time, event.get('summary')
        summary = event.get('summary')
        if summary == None:
            summary = 'no summary'
        ret['events'].append({'summary':summary,'start':start_time}) 
        #datetime.datetime.strftime(start_time,'%a %H:%M'), 'datetime':start_time})
    return ret

def get_all():
    creds = auth()
    #bit of a hack
    primary = fetch(creds,'primary')
    inma = fetch(creds,'inmapiquerasramos@gmail.com')
    primary['events'] += inma['events']
    primary['events'].sort()
    return primary

if __name__ == "__main__":
    print get_all()
