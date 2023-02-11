# Project Time Tracking using Calendar Events

## Requirements

- integrate with calendar
- only use standard calendar features
- use standard calendar to modify entries or add entries afterwards
- use from my PC computer only, no need for mobile app
- use my existing StreamDeck, so it is in my face and does not need extra screen estate

- start time logging
	- press button on StreamDeck. one button per project (they don't change that often and there are not that many)
	- pass project name as command line argument (makes it easy to change)
  - use currenct time as start time (i want it accurate to the minute)
	- use projectname as titel and tag
  - create calendar event with duration of 2 hours (just to be safe, it is already online)
	- store the ID of the created event localy
- stop logging
	- show popup with titel and current_time - start_time duration
  - ask me for details about the work in this simple popup window
  - UPDATE event(eventId) with current_time as end_time and comment as body.content


## gmail
Using *gmail* sounded like the simplest answer:
there is a good API description and *python code examples*:
https://developers.google.com/calendar/api/v3/reference/events/insert#examples
it links to Python quickstart on how to setup the environment:
https://developers.google.com/calendar/quickstart/python
and that is where i stopped, because it asked for a *google cloud project* and a *google workspace*. it sounded too complicated and like something that might ask for my credit card.

## outlook
since i use *Microsoft365* (shame on me: it should be an FOSS solution, but oh my) let us try this.
Looks like i need to the use *Graph REST API*. Documentation is straight forward.
https://learn.microsoft.com/en-us/graph/api/event-update?view=graph-rest-1.0&tabs=http
but.... code examples are not available in python.

## chatGPT
chatGPT to the rescue! Let us play and see what it can do.
took me 10 minutes to ask for code step by step. (dry run, i did not dare to actually try it just yet.)
conversation is available here: *chatPGT_conversation.md*
ChatGPT Queries also available via GIT commit history.

## environment
i run this on a Win10 machine. Python 3.8.0
