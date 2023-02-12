import requests
import datetime
import pytz

# Microsoft Graph endpoint for creating an event
endpoint = "https://graph.microsoft.com/v1.0/me/events"

# Access token for authentication
# Load the access token from the text file
with open("private_access_token.txt", "r") as file:
    access_token = file.read().strip()

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
headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json"
}

response = requests.post(endpoint, headers=headers, json=event)

# Check the response status code
if response.status_code != 201:
    raise Exception("Failed to create event: " + response.text)

# Get the newly created event from the response
event = response.json()
print("Event created successfully:", event)
