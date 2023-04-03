import requests
from datetime import datetime, timedelta, timezone
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT
import configparser
import json
import PySimpleGUI as sg
import sys

# load config file (offloaded for privacy reasons)
config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])

APP_ID = config['azure']['appId']
SCOPES = ['Calendars.ReadWrite']

# Generate Access Token
access_token = generate_access_token(APP_ID, SCOPES)
headers = {
    'Authorization': 'Bearer ' + access_token['access_token'],
    "Content-Type": "application/json"
}

# Microsoft Graph endpoint for creating an event
CAL_ID = config['calendar']['calId']
endpoint = f'https://graph.microsoft.com/v1.0/me/calendars/{CAL_ID}/events?'


# Get the event subject/titel from the command line
if len(sys.argv) < 2:
    # no title - so show everything in past month
    # TODO: calc start and endtime of the (current month or if 1st-3rd then of the last month (with buffer)
    # Get the current system time
    now = datetime.now(timezone.utc)
    # standardize to UTC.. so it is always true. since we always create it from NOW.
    start_time = now.isoformat()
    #end_time = (now + datetime.timedelta(hours=2)).isoformat()
    #endpoint += "and start/dateTime ge '2023-04-01T00:00'"

else:
    subject = sys.argv[1]
    endpoint += f"$filter=startsWith(subject,'{subject}')"

endpoint += "&$select=subject,bodyPreview,start,end"
endpoint += "&$orderby=start/dateTime asc"
# https://learn.microsoft.com/en-us/graph/query-parameters?tabs=http

