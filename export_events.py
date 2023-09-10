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

endpoint += "&$select=subject,location,bodyPreview,start,end"
endpoint += "&$orderby=start/dateTime asc"
# https://learn.microsoft.com/en-us/graph/query-parameters?tabs=http

events = []
# make get requests till there are no more events
while endpoint:
    #print("endpoint: ", endpoint[-40:])
    # Make a GET request to the Microsoft Graph API to retrieve the event
    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to retrieve event: " + response.text)

    #print("successfully received "+ str(len(response.json()['value'])) + " events")
    events += response.json()['value']

    endpoint = response.json().get("@odata.nextLink") # returns link or 'None'


print("Received a total of "+ str(len(events)) + " events")
# print(json.dumps(events, indent=2))
print("")

total_time = timedelta()

for event in events:
    # Calculate the elapsed time since the event start
    start_time_notz = datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S.%f0")
    start_time = start_time_notz.replace(tzinfo=timezone.utc)
    end_time_notz = datetime.strptime(event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S.%f0")
    end_time = end_time_notz.replace(tzinfo=timezone.utc)
    elapsed_time = end_time - start_time
    hours, remainder = divmod(int(elapsed_time.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)
    total_time += elapsed_time
    body_preview_cleaned = ' '.join(event["bodyPreview"].splitlines())[:50]

    print(
        event["start"]["dateTime"][0:10] + "; " +
        f"{int(hours):>2}h{int(minutes):02}" + "; " +
        event["subject"].strip() + "; " +
        event["location"]["displayName"].strip() + "; " +
        body_preview_cleaned + "; "
    )

print("")
hours, remainder = divmod(int(total_time.total_seconds()), 3600)
minutes, _ = divmod(remainder, 60)
print(f"Total time: {int(hours)} hours, {int(minutes)} minutes")
