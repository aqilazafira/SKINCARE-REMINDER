import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

SCOPES = ["https://www.googleapis.com/auth/calendar"]
DAYS = ["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"]
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

DAY_TO_BYDAY = {
    "SENIN": "MO", "SELASA": "TU", "RABU": "WE",
    "KAMIS": "TH", "JUMAT": "FR", "SABTU": "SA", "MINGGU": "SU"
}

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                raise Exception("Refresh token expired. Generate token.json baru di lokal.")
        else:
            # Jika di server tidak ada token, langsung throw error.
            # Jangan panggil run_local_server di sini karena akan bikin freeze.
            raise Exception("token.json tidak ditemukan! Upload file token.json ke server.")

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds

def get_next_weekday(day_index):
    today = datetime.now()
    days_ahead = day_index - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return today + timedelta(days=days_ahead)

def save_calendar_event(day, time, email):
    try:
        service = build("calendar", "v3", credentials=get_credentials())
        next_occurrence = get_next_weekday(day)
        event_start = datetime.strptime(f"{next_occurrence.date()} {time}", "%Y-%m-%d %H:%M")
        event_end = event_start + timedelta(hours=1)
        byday = DAY_TO_BYDAY.get(DAYS[day].upper(), "FR")

        event = {
            "summary": "Skincare Reminder",
            "location": "Home",
            "description": "Time to take care of your skin",
            "colorId": 6,
            "start": {"dateTime": event_start.isoformat(), "timeZone": "Asia/Jakarta"},
            "end": {"dateTime": event_end.isoformat(), "timeZone": "Asia/Jakarta"},
            "recurrence": [f"RRULE:FREQ=WEEKLY;COUNT=4;BYDAY={byday}"],
            "attendees": [{"email": email}],
        }
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as error:
        print(f"Error save_event: {error}")

def update_calendar_event(event_id, day, time, email):
    try:
        service = build("calendar", "v3", credentials=get_credentials())
        next_occurrence = get_next_weekday(day)
        event_start = datetime.strptime(f"{next_occurrence.date()} {time}", "%Y-%m-%d %H:%M")
        event_end = event_start + timedelta(hours=1)
        byday = DAY_TO_BYDAY.get(DAYS[day].upper(), "FR")

        event = service.events().get(calendarId="primary", eventId=event_id).execute()
        event['start']['dateTime'] = event_start.isoformat()
        event['end']['dateTime'] = event_end.isoformat()
        event['recurrence'] = [f"RRULE:FREQ=WEEKLY;COUNT=4;BYDAY={byday}"]
        event['attendees'] = [{"email": email}]

        updated_event = service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
        print(f"Event updated: {updated_event.get('htmlLink')}")
    except Exception as error:
        print(f"Error update_event: {error}")

def delete_calendar_event(event_id):
    try:
        service = build("calendar", "v3", credentials=get_credentials())
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print("Event deleted")
    except Exception as error:
        print(f"Error delete_event: {error}")
