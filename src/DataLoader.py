import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

def LoadData(uploadedFile):
    try:
        if uploadedFile.name.endswith(".csv"):
            data = pd.read_csv(uploadedFile)
        elif uploadedFile.name.endswith(".xlsx"):
            data = pd.read_excel(uploadedFile, engine="openpyxl")
        else:
            raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")
        return data
    except Exception as e:
        return str(e)

    
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

clientSecret = os.getenv("GOOGLE_CLIENT_SECRET")

import json

def LoadGoogleSheet(sheetURL):
    try:
        creds_content = os.getenv("GOOGLE_CLIENT_SECRET")
        if creds_content.startswith("{"):
            creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_content), scope)
        else:
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_content, scope)

        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheetURL)

        worksheet_list = sheet.worksheets()
        worksheet_names = [ws.title for ws in worksheet_list]

        st.write("Available Worksheets:", worksheet_names)
        selected_worksheet = st.selectbox("Select Worksheet", worksheet_names)

        worksheet = sheet.worksheet(selected_worksheet)
        data = worksheet.get_all_records()

        headers = worksheet.row_values(1) 
        if len(headers) != len(set(headers)):
            st.warning("Duplicate headers detected in the worksheet.")
            headers = pd.io.parsers.ParserBase({'names': headers})._maybe_dedup_names(headers)
            data = pd.DataFrame(worksheet.get_all_values()[1:], columns=headers)

            st.info(f"Headers were deduplicated: {headers}")
        else:
            data = pd.DataFrame(data)

        if not data.empty:
            return data
        else:
            st.warning("The selected worksheet is empty.")
            return pd.DataFrame()

    except Exception as e:
        raise ValueError(f"Error loading Google Sheet: {e}")


def loadCSV(file):
    return pd.read_csv(file)




SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 
          'https://www.googleapis.com/auth/spreadsheets.readonly']

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os


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