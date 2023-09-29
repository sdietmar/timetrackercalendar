import requests
from datetime import datetime, timedelta, timezone
import tzlocal
import calendar
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT
import configparser
import json
import PySimpleGUI as sg
import sys
import argparse

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


# Get the event subject/title from the command line
# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Export events from calendar. filter by subject and limit the daterange')

# Define the command-line arguments
parser.add_argument('--subject', default='', help='Filter by subject')
parser.add_argument('--months', default='this', choices=['this', 'last', 'all'], help='Date filter for months')

# Parse the command-line arguments
args = parser.parse_args()

# subject filter
endpoint += f"$filter=startsWith(subject,'{args.subject}')"

# time span filter
timespan = args.months
today = datetime.now()

# Determine the start and end dates based on the "this" or "last" argument
if timespan == "this":
    start_date = today.replace(day=1)
    _, last_day = calendar.monthrange(today.year, today.month)
    end_date = today
elif timespan == "last":
    # Calculate the first day of the last month
    last_month = today - timedelta(days=today.day)
    start_date = last_month.replace(day=1)
    _, last_day = calendar.monthrange(last_month.year, last_month.month)
    end_date = last_month.replace(day=last_day)
elif timespan == "all":
    #safeguard
    start_date = today
    end_date = today
else:
    print("Invalid value for the second argument. Use 'this', 'last' or 'all'.")
    sys.exit(1)

if timespan != 'all':
    endpoint += f" and start/dateTime ge '{start_date.strftime('%Y-%m-%d')}T00:00:00Z'"
    endpoint += f" and end/dateTime le '{end_date.strftime('%Y-%m-%d')}T23:59:59Z'"


endpoint += "&$select=subject,location,bodyPreview,start,end"
endpoint += "&$orderby=start/dateTime asc"
# https://learn.microsoft.com/en-us/graph/query-parameters?tabs=http

# print(endpoint)

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

# Get the local timezone
local_timezone = tzlocal.get_localzone()

for event in events:
    #get time and adjust to local time
    start_time_notz = datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S.%f0")
    start_time_e = start_time_notz.replace(tzinfo=local_timezone)
    start_time = start_time_e + start_time_e.utcoffset()
    end_time_notz = datetime.strptime(event["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S.%f0")
    end_time_e = end_time_notz.replace(tzinfo=local_timezone)
    end_time = end_time_e + end_time_e.utcoffset()

    # Calculate the elapsed time since the event start
    elapsed_time = end_time - start_time
    hours, remainder = divmod(int(elapsed_time.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)
    total_time += elapsed_time

    # is it another day?
    days = (end_time.date() - start_time.date()).days
    if days == 0: days_t = ''
    else: days_t = f"{days}:"


    print(
        f"{start_time.strftime('%Y-%m-%d; %H:%M')};" +
        (days_t + f"{end_time.strftime('%H:%M')}; ").rjust(10) +
        f"{int(hours):>2}h{int(minutes):02}" + "; " +
        event["subject"].strip() + "; " +
        event["location"]["displayName"].strip()[:24].ljust(24) + "; " +
        body_preview_cleaned
    )

print("")
hours, remainder = divmod(int(total_time.total_seconds()), 3600)
minutes, _ = divmod(remainder, 60)
print(f"Invested time: {int(hours)} hours, {int(minutes)} minutes")

# how many workdays in range?
workdays = 0
current_date = start_date
# Define a list of weekend days (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
weekend_days = [5, 6]  # Saturday (5) and Sunday (6)
while current_date <= end_date:
    # Check if the current day is not a weekend day (not in weekend_days)
    if current_date.weekday() not in weekend_days:
        workdays += 1
    current_date += timedelta(days=1)

# expected worked hours
exp_hrs_per_day = 38.5 / 5
exp_hrs_total = workdays * exp_hrs_per_day
hours, remainder = divmod(exp_hrs_total, 1)
minutes = int(remainder*60)

print(f"Expected time: {int(hours)} hours, {int(minutes)} minutes")
print(f"{workdays} workdays between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}")
