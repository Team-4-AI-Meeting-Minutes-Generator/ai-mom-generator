import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/meetings.space.readonly",
    "https://www.googleapis.com/auth/calendar.events.readonly"
]

def get_google_meet_service():
    """
    Authenticates the user and returns a Google Meet API service instance.
    Assumes credentials.json is in the same directory.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("src/credentials.json"):
                print("Error: src/credentials.json not found. Please follow meet_setup_guide.md.")
                return None
                
            flow = InstalledAppFlow.from_client_secrets_file(
                "src/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("meet", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def list_recent_conferences():
    """
    Lists recent Google Meet conferences.
    """
    service = get_google_meet_service()
    if not service:
        return []

    try:
        # Note: This is a simplified example. You might want to filter or paginate.
        results = service.conferenceRecords().list().execute()
        return results.get("conferenceRecords", [])
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def get_transcript(conference_record_name):
    """
    Retrieves the transcript entries for a specific conference record.
    """
    service = get_google_meet_service()
    if not service:
        return ""

    try:
        transcripts = service.conferenceRecords().transcripts().list(parent=conference_record_name).execute()
        full_text = ""
        for transcript in transcripts.get("transcripts", []):
            entries = service.conferenceRecords().transcripts().entries().list(parent=transcript["name"]).execute()
            for entry in entries.get("transcriptEntries", []):
                full_text += f"{entry.get('participant', 'Unknown')}: {entry.get('text', '')}\n"
        
        return full_text
    except HttpError as error:
        print(f"An error occurred: {error}")
        return ""

if __name__ == "__main__":
    # Test listing
    conferences = list_recent_conferences()
    for conf in conferences:
        print(f"Found Conference: {conf['name']} at {conf['startTime']}")
