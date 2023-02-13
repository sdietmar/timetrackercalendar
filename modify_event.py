import requests
import datetime
import pytz
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT
import configparser
import json

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
    'Authorization': 'Bearer ' + access_token['access_token'],
    "Content-Type": "application/json"
}


# Load the event data from the JSON file
with open("event.json", "r") as file:
    event_data = json.load(file)

# Get the event ID from the loaded data
event_id = event_data["event_id"]

# Microsoft Graph endpoint for creating an event
CAL_ID = config['calendar']['calId']
endpoint = f'https://graph.microsoft.com/v1.0/me/calendars/{CAL_ID}/events/{event_id}'
# f'/users/{id | userPrincipalName}/calendars/{id}/events


# Make a GET request to the Microsoft Graph API to retrieve the event
response = requests.get(endpoint, headers=headers)

# Check the response status code
if response.status_code != 200:
    raise Exception("Failed to retrieve event: " + response.text)

# Get the updated event from the response
event = response.json()
print("Event retrieved successfully:", event)

