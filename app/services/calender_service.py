import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

DAYS = ["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"]

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "token.json")

# Mapping of day names to BYDAY values
DAY_TO_BYDAY = {
    "SENIN": "MO",
    "SELASA": "TU",
    "RABU": "WE",
    "KAMIS": "TH",
    "JUMAT": "FR",
    "SABTU": "SA",
    "MINGGU": "SU"
}

def get_next_weekday(day):
    today = datetime.now()
    days_ahead = day - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)

def save_calendar_event(day, time, email):
    creds = None

    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(CREDENTIALS_FILE, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Calculate the next occurrence of the specified day
        next_occurrence = get_next_weekday(day)
        event_start = datetime.strptime(f"{next_occurrence.date()} {time}", "%Y-%m-%d %H:%M")
        event_end = event_start + timedelta(hours=1)  # Assuming the event lasts 1 hour

        # Get the BYDAY value for the specified day
        byday = DAY_TO_BYDAY.get(DAYS[day].upper(), "FR")  # Default to Friday if day is not found

        event = {
            "summary": "Skincare Reminder",
            "location": "Home",
            "description": "Time to take care of your skin",
            "colorId": 6,
            "start": {
                "dateTime": event_start.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": event_end.isoformat(),
                "timeZone": "UTC",
            },
            "recurrence": [
                f"RRULE:FREQ=WEEKLY;COUNT=4;BYDAY={byday}",
            ],
            "attendees": [
                {"email": email},
            ],
        }

        event = service.events().insert(calendarId="primary", body=event).execute()

        print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print("An error occurred:", error)

def update_calendar_event(event_id, day, time, email):
    creds = None

    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(CREDENTIALS_FILE, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Calculate the next occurrence of the specified day
        next_occurrence = get_next_weekday(day)
        event_start = datetime.strptime(f"{next_occurrence.date()} {time}", "%Y-%m-%d %H:%M")
        event_end = event_start + timedelta(hours=1)  # Assuming the event lasts 1 hour

        # Get the BYDAY value for the specified day
        byday = DAY_TO_BYDAY.get(DAYS[day].upper(), "FR")  # Default to Friday if day is not found

        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        event['start']['dateTime'] = event_start.isoformat()
        event['end']['dateTime'] = event_end.isoformat()
        event['recurrence'] = [f"RRULE:FREQ=WEEKLY;COUNT=4;BYDAY={byday}"]
        event['attendees'] = [{"email": email}]

        updated_event = service.events().update(calendarId="primary", eventId=event_id, body=event).execute()

        print(f"Event updated: {updated_event.get('htmlLink')}")

    except HttpError as error:
        print("An error occurred:", error)

def delete_calendar_event(event_id):
    creds = None

    if os.path.exists(CREDENTIALS_FILE):
        creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(CREDENTIALS_FILE, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print("Event deleted")

    except HttpError as error:
        print("An error occurred:", error)
