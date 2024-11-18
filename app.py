import streamlit as st
from src.DataLoader import LoadData, LoadGoogleSheet
import pandas as pd
from src.LLMParsing import LLMFunction
from src.WebSearchForLLM import GetInsights
from src.UpdateDataframe import CleanedResponse

st.title("IntelFlow - AI-Powered Company Information Search")

if 'data' not in st.session_state:
    st.session_state.data = None
if 'search_prompt' not in st.session_state:
    st.session_state.search_prompt = ""
if 'search_result' not in st.session_state:
    st.session_state.search_result = None

dataSource = st.radio("Select the data source", ["Upload File", "Google Sheet"])

if dataSource == "Upload File":
    uploadedFile = st.file_uploader("Upload a CSV or Excel file with Company Names", type=["csv", "xlsx"])
    if uploadedFile:
        st.session_state.data = LoadData(uploadedFile)
        st.success("File loaded successfully!")

elif dataSource == "Google Sheet":
    sheetURL = st.text_input("Enter the full Google Sheet URL", value="")
    if st.button("Load Sheet") and sheetURL:
        try:
            st.session_state.data = LoadGoogleSheet(sheetURL)
            st.success("Data loaded successfully from Google Sheet!")
        except Exception as e:
            st.error(f"Error loading Google Sheet: {e}")

if st.session_state.data is not None and not st.session_state.data.empty:
    st.write("Data Preview:")
    st.dataframe(st.session_state.data.head())

    st.session_state.search_prompt = st.text_input("Enter your prompt (e.g., 'Get the email of {company}')", value=st.session_state.search_prompt)

    if st.session_state.search_prompt.strip():
        if st.button("Search"):
            if st.session_state.data is None or st.session_state.search_prompt.strip() == "":
                st.error("Please upload data and enter a valid search prompt.")
            else:
                if st.session_state.search_result is None:
                    st.write("Searching for information...")
                    result = LLMFunction(st.session_state.search_prompt)
                    st.write(result) 
                    st.session_state.search_result = result 
                else:
                    st.write("Result already found, using stored data.")
                    result = st.session_state.search_result 
                
                if result is not None:
                    cleanedResponse = CleanedResponse(result)
                    st.write(cleanedResponse) 

                    if cleanedResponse is not None and not cleanedResponse.empty:
                        st.write("Cleaned Response:")
                        
                        CSVData = cleanedResponse.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=CSVData,
                            file_name="results.csv",
                            mime="text/csv"
                        )
                        st.success("Thank You")
                    else:
                        st.error("No valid cleaned response was generated.")
