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


