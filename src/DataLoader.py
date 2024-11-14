import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os


def LoadData(CSVFile):
    try:
        data = pd.read_csv(CSVFile)

        return data
    except Exception as e:
        return str(e)
    
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 
          'https://www.googleapis.com/auth/spreadsheets.readonly']

def AuthenticateUser():
    load_dotenv()
    try:
        clientSecretFile = os.getenv('OAUTH_CREDENTIALS_PATH')
        print(f"Google Client Secret Path: {clientSecretFile}")

        if not clientSecretFile:
            raise ValueError("Missing GOOGLE_CLIENT_SECRET environment variable")
    except Exception as e:
        raise ValueError(f"Error loading GOOGLE_CLIENT_SECRET: {e}")
    

    flow = InstalledAppFlow.from_client_secrets_file(
        clientSecretFile, SCOPES)
    
    flow.redirect_uri = 'http://localhost:8501'

    creds = flow.run_local_server(port=8501)
    
    driveService = build('drive', 'v3', credentials=creds)
    sheetsService = build('sheets', 'v4', credentials=creds)
    return driveService, sheetsService

def ListGoogleSheets(drive_service):
    results = drive_service.files().list(
        q="mimeType='application/vnd.google-apps.spreadsheet'",
        pageSize=10, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items

def LoadGoogleSheetData(sheets_service, sheet_id, sheet_range="Sheet1"):
    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    values = result.get('values', [])
    if values:
        df = pd.DataFrame(values[1:], columns=values[0])
    else:
        df = pd.DataFrame()
    return df