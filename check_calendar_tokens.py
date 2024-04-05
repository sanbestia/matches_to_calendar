# check validity of stored tokens
# if not present, create token file

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES: list[str] = ["https://www.googleapis.com/auth/calendar"]


def check_calendar_tokens() -> Credentials:
    print("Checking tokens...")
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path="token.json"):
        creds = Credentials.from_authorized_user_file(filename="token.json", scopes=SCOPES)
        print("Tokens exist")
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("No valid tokens available, creating new ones")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow: InstalledAppFlow = (InstalledAppFlow.from_client_secrets_file(
                client_secrets_file="credentials.json",
                scopes=SCOPES
            ))
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            print("Tokens created")
    else:
        print("Available tokens are valid")
    print()
    return creds


def main():
    pass


if __name__ == '__main__':
    main()
