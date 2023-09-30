from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '17T0_C1qq106np76U2C5xDVb5NaS_PiYEm11gG-AG0HY'
SAMPLE_RANGE_NAME = 'A1:E3'
sheet=""


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        global sheet
        sheet = service.spreadsheets()
    except HttpError as err:
        print(err)

def get_all_stocks():
    main()
    ret=[]
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='A2:A').execute()
    values = result.get('values', [])
    if not values:
        print('no symbols found')
        return ret
    
    for row in values:
        ret.append(row[0])
    return ret

def get_stock_details(stock:str):
    main()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='A2:J').execute()
    values = result.get('values',[])
    if not values:
        return []
    for row in values:
        if (row[0].upper()==stock.upper()):
            return row


if __name__ == '__main__':
    main()
    print(get_stock_details("piind"))