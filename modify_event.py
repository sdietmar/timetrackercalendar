import requests
import datetime
import pytz
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


# Calculate the elapsed time since the event start
start_time_notz = datetime.datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S.%f0")
start_time = start_time_notz.replace(tzinfo=datetime.timezone.utc)
current_time = datetime.datetime.now(datetime.timezone.utc)
elapsed_time = current_time - start_time
#timezone madness. i hardcode/standardize everything to UTC!
#print (event["start"]["dateTime"])
#print(start_time)
#print(start_time_notz)
#print(current_time)
#print(elapsed_time)
hours, remainder = divmod(int(elapsed_time.total_seconds()), 3600)
minutes, _ = divmod(remainder, 60)

# Create the PySimpleGUI popup
layout = [
    [sg.Text("Event Subject: " + event["subject"])],
    [sg.Text("Elapsed Time: {} hours {} minutes".format(hours, minutes))],
    [sg.Text("Event Body:", size=(15, 1)), sg.InputText("")],
    [sg.Button("Update Event"), sg.Button("Cancel")]
]

window = sg.Window("Update Event", layout)

# Show the popup and get the user input
while True:
    clickevent, values = window.read()
    if clickevent in (None, "Cancel"):
      # exits the program
      sys.exit("User aborted... closing without any changes")
    if clickevent == "Update Event":
      print(values[0])
      break
window.close()

print(values[0]) # i dont understand why this variable is available here? not part of the loop?

current_time = datetime.datetime.now(datetime.timezone.utc)

# Make a PATCH request to the Microsoft Graph API to update the event
body = {
    "body": {
        "content": values[0]
    },
    "end": {
        "dateTime": current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "timeZone": "UTC"
    }
}

response = requests.patch(endpoint, headers=headers, json=body)

# Check the response status code
if response.status_code != 200:
    raise Exception("Failed to update event: " + response.text)

print("Event updated successfully")