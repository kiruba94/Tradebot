from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gc
from memory_profiler import profile
gc.set_threshold(0)
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
    credentials = service_account.Credentials.from_service_account_file("Credentials.json", scopes=SCOPES)
    try:
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except HttpError as err:
        return None

def get_all_stocks():
    service = main()
    if service==None:
        return None
    sheet= service.spreadsheets()
    del service
    ret=[]
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='A2:A').execute()
    del sheet
    gc.collect()
    values = result.get('values', [])
    if not values:
        print('no symbols found')
        return None

    for row in values:
        ret.append(row[0])
    return ret

def get_stock_details(stock:str):
    service = main()
    if service==None:
        return None
    sheet= service.spreadsheets()
    del service
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range='A2:J').execute()
    del sheet
    gc.collect()
    values = result.get('values',[])
    if not values:
        return None
    for row in values:
        if (row[0].upper()==stock.upper()):
            return row


if __name__ == '__main__':
    main()
    print(get_stock_details("piind"))      