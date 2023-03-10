import requests
import datetime
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT
import configparser
import json
import sys
import time

# load config file (offloaded for privacy reasons)
config = configparser.ConfigParser()
config.read(['config.cfg', 'config.dev.cfg'])

APP_ID = config['azure']['appId']
SCOPES = ['Calendars.ReadWrite']


# this stuff works. could not get ms examples to work with cache
# https://learndataanalysis.org/source-code-create-and-delete-outlook-calendar-events-using-microsoft-graph-api-in-python/
# Generate Access Token
access_token = generate_access_token(APP_ID, SCOPES)
headers = {
    'Authorization': 'Bearer ' + access_token['access_token']
}

# Microsoft Graph endpoint for creating an event
CAL_ID = config['calendar']['calId']
endpoint = f'https://graph.microsoft.com/v1.0/me/calendars/{CAL_ID}/events'
# f'/users/{id | userPrincipalName}/calendars/{id}/events


# Get the current system time
now = datetime.datetime.now(datetime.timezone.utc)
# standardize to UTC.. so it is always true. since we always create it from NOW.

# Set the start and end time for the event
start_time = now.isoformat()
end_time = (now + datetime.timedelta(hours=2)).isoformat()

# Get the event subject/titel from the command line
if len(sys.argv) < 2:
    #print("Usage: python create_event.py <subject>")
    subject = "Work"
else:
    subject = sys.argv[1]

# Event details
event = {
    "subject": subject,
    "body": {
        "contentType": "text"
    },
    "start": {
        "dateTime": start_time,
        "timeZone": "UTC"
    },
    "end": {
        "dateTime": end_time,
        "timeZone": "UTC"
    },
    "isReminderOn": False,
    "categories": ["timetracker"]
}

# Make a POST request to the Microsoft Graph API to create the event
response = requests.post(endpoint, headers=headers, json=event)

# Check the response status code
if response.status_code != 201:
    raise Exception("Failed to create event: " + response.text)

# Get the newly created event from the response
event = response.json()
print("Started logging time for:", subject)

# Save the event ID to a dictionary
event_data = {"event_id": event["id"]}

# Write the event data to a JSON file
with open("event.json", "w") as file:
    json.dump(event_data, file)

time.sleep(2)    # Pause to give user time to read
