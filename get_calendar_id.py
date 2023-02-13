import requests
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT
import configparser
import json
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
    'Authorization': 'Bearer ' + access_token['access_token']
}

# Microsoft Graph endpoint for creating an event
CAL_ID = config['calendar']['calId']
endpoint = 'https://graph.microsoft.com/v1.0/me/calendars'
# f'/users/{id | userPrincipalName}/calendars/{id}

response = requests.get(endpoint, headers=headers)

print(response.json())
# look for "id" where the "name" is what you expect