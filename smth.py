import streamlit as st
from src.DataLoader import LoadData, AuthenticateUser, ListGoogleSheets, LoadGoogleSheetData

st.title("IntelFlow - AI-Powered Company Information Search")
dataSource = st.radio("Select the data source", ["Upload File", "Google Sheet"])

print(st.session_state)

if dataSource == "Upload File":
    uploadedFile = st.file_uploader("Upload a CSV file with Company Names", type=["csv", "xlsx"])

    if uploadedFile:
        data = LoadData(uploadedFile)
        st.write("Data Preview: ", data.head())

        column = st.selectbox("Select the column with Company Names", data.columns)

        searchPrompt = st.text_input("Enter your prompt (e.g., 'Get the email of {company}')")

        if st.button("Search"):
            st.write("Searching for information... ")

elif dataSource == "Google Sheet":
    
    st.title("Browse and Load Google Sheets from Google Drive")

    if st.button("Authenticate and Browse Google Drive"):

        driveService, sheetsService =st.session_state.data =  AuthenticateUser()

        sheetsList = ListGoogleSheets(driveService)
        selectedSheet = st.selectbox("Select a Google Sheet", sheetsList, format_func=lambda x: x['name'])

        if selectedSheet:
            sheetID = selectedSheet['id']
            sheetRange = st.text_input("Enter Sheet Range (default: Sheet1)", "Sheet1")

            if st.button("Load Google Sheet"):
                data = LoadGoogleSheetData(sheetsService, sheetID, sheetRange)
                st.write("Data Preview: ", data.head())

                column = st.selectbox("Select the column with Company Names", data.columns)

                searchPrompt = st.text_input("Enter your prompt (e.g., 'Get the email of {company}')")

                if st.button("Search"):
                    st.write("Searching for information... ")
