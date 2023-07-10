from dotenv import load_dotenv
from Emailer import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from ics import Calendar, Event
from dateutil import tz
import os, json
from dotenv import load_dotenv
from Emailer import *
import os, json
import datetime
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from ics import Calendar, Event
from dateutil import tz
from Slack_Messenger import *
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

def create_event_with_dates(summary, location, description, start_time, end_time):
    # Define the scopes for the Google Calendar API
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, access_type='offline')

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the service
    service = build('calendar', 'v3', credentials=creds)

    # Define the event
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'date': start_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'date': end_time,
            'timeZone': 'America/Los_Angeles',
        },
        'visibility': 'public',  # Make the event public
    }

    # Call the Calendar API to create the event
    event = service.events().insert(calendarId='primary', body=event).execute()

    # Return the link to the event
    return event['htmlLink']

def create_event(summary, location, description, start_time, end_time):
    # Define the scopes for the Google Calendar API
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, access_type='offline')

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the service
    service = build('calendar', 'v3', credentials=creds)

    # Define the event
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',
        },
        'visibility': 'public',  # Make the event public
    }

    # Call the Calendar API to create the event
    event = service.events().insert(calendarId='primary', body=event).execute()

    # Return the link to the event
    return event['htmlLink']

def send_slack_message_with_calendar_link(summary, location, description, start_time, end_time, message, slack_channel="general"):
    # Create Google Calendar event and get the link
    event_link = create_event(summary, location, description, start_time, end_time)

    # Send message that the alarm system is activated
    Slacker = Slack_er()
    message_with_link = f"{message}\n\nAdd to your Google Calendar :spiral_calendar_pad:: {event_link}"
    Slacker.send_message(slack_channel, message_with_link)

def send_slack_message(message,slack_channel="general"):
    # Send message that the alarm system is activated
    Slacker = Slack_er()
    Slacker.send_message(slack_channel, message)

def send_email_with_calendar_invite(recipient_email, subjectLine, content, p_date, p_time):
    # Create a calendar event
    event = Event()

    # Get the local timezone
    local_tz = tz.gettz('America/Los_Angeles')  # Replace with your actual timezone

    # Set the event begin time with the timezone
    event.begin = '{}T{}:00'.format(p_date, p_time)
    event.begin = event.begin.replace(tzinfo=local_tz)

    # Set event name
    event.name = subjectLine.replace("Reminder ","")

    # Add the event to a calendar
    calendar = Calendar(events=[event])

    # Convert the event to an ics string
    ics_string = str(calendar)

    # send email to lab maintainer with the calendar invite attached
    send_email_invite(recipient_email, subjectLine, content, ics_string)




def send_email_with_calendar_invite(recipient_email, subjectLine, content, p_date, p_time):
    # Create a calendar event
    event = Event()

    # Get the local timezone
    local_tz = tz.gettz('America/Los_Angeles')  # Replace with your actual timezone

    # Set the event begin time with the timezone
    event.begin = '{}T{}:00'.format(p_date, p_time)
    event.begin = event.begin.replace(tzinfo=local_tz)

    # Set event name
    event.name = subjectLine.replace("Reminder ","")

    # Add the event to a calendar
    calendar = Calendar(events=[event])

    # Convert the event to an ics string
    ics_string = str(calendar)

    # send email to lab maintainer with the calendar invite attached
    send_email_invite(recipient_email, subjectLine, content, ics_string)

def create_reminder(instruction):
    check_symbol = "-"
    # check_symbol = "-"
    return "{} {}\n".format(check_symbol, instruction)

def create_step(reminder):
    check_symbol = "☐"
    # check_symbol = "-"
    return "{} {}\n".format(check_symbol, reminder)

def get_header(name, date_maintenance):
    header = "Hi {},\n\nThis is a reminder that tomorrow ({}) is your turn to do the LFL Lab Maintenance. Please refer to the following checklist.\n\n".format(name, date_maintenance)
    return header

def get_signature(bot_name="LFL Bot"):
    salute = "🫡 "
    # salute = ""
    return "\n\nThank you for your service {},\n{}".format(salute, bot_name)

def get_reminders(reminders_list):
    reminders = []
    for reminder_string in reminders_list:
        reminders.append(create_reminder(reminder_string))
    prompt = "\n\nSome safety considerations from EH&S:\n"
    reminders = "".join(reminders)
    return prompt + reminders + "\n"


def create_email_content(name, date_maintenance, instructions, reminders, bot_name="LFL Bot"):
    header = get_header(name, date_maintenance)
    steps = []
    for instruction in instructions:
        steps.append(create_step(instruction))
    body = "".join(steps)
    reminders = get_reminders(reminders)
    signature = get_signature(bot_name)
    return header + body + reminders + signature

def extract_lab_maintainer():
    load_dotenv(".env")
    user_id = str(os.environ.get("USER_ID"))
    user_name, user_email = get_user_info(user_id)
    return user_name, user_email

def get_user_info(user_id):
    f = open("lab_members.json")
    data = json.load(f)
    user_name, user_email = data[user_id]["name"], data[user_id]["email"]
    return user_name, user_email

def get_last_user_id():
    f = open("lab_members.json")
    data = json.load(f)
    id_num = int(list(data.keys())[-1])
    return id_num

def send_email(email,subjectLine, emailContent):
    sms_list = ['']
    sender = Emailer(email, sms_list, subjectLine, emailContent)
    sender.send_email()

def update_record(f=".env"):
    # Read in the file
    load_dotenv(f)
    last_id = get_last_user_id()

    with open(f, 'r') as file :
        filedata = file.read()

    # Replace the target string
    user_id = int(os.environ.get("USER_ID"))
    target = "ID="+str(user_id)

    if user_id != last_id:
        update = "ID="+str(user_id+1)
    else:
        update = "ID="+str(1)

    filedata = filedata.replace(target, update)

    # Write the file out again
    with open(f, 'w') as file:
        file.write(filedata)
