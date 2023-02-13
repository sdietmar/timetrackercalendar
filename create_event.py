import requests
import datetime
import pytz
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT

with open("private_app_id.txt", "r") as file:
    APP_ID = file.read().strip()

SCOPES = ['Calendars.ReadWrite']


# this stuff works. could not get ms examples to work with cache
# https://learndataanalysis.org/source-code-create-and-delete-outlook-calendar-events-using-microsoft-graph-api-in-python/
# Generate Access Token
access_token = generate_access_token(APP_ID, SCOPES)
headers = {
    'Authorization': 'Bearer ' + access_token['access_token']
}

# Microsoft Graph endpoint for creating an event
endpoint = "https://graph.microsoft.com/v1.0/me/events"


# Get the current system time
now = datetime.datetime.now(pytz.UTC)

# Set the start and end time for the event
start_time = now.isoformat()
end_time = (now + datetime.timedelta(hours=2)).isoformat()

# Event details
event = {
    "subject": "Sample event",
    "start": {
        "dateTime": start_time,
        "timeZone": "UTC"
    },
    "end": {
        "dateTime": end_time,
        "timeZone": "UTC"
    }
}

# Make a POST request to the Microsoft Graph API to create the event
response = requests.post(endpoint, headers=headers, json=event)

# Check the response status code
if response.status_code != 201:
    raise Exception("Failed to create event: " + response.text)

# Get the newly created event from the response
event = response.json()
print("Event created successfully:", event)
