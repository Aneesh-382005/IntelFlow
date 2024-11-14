import pandas as pd
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import re

load_dotenv()

emailPattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
addressPattern = re.compile(r'\d{1,5}\s[\w\s]+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Way|Square|Sq)\b')
phonePattern = re.compile(r'(\(?\+?[0-9]*\)?)?(\s|-|\.)?[0-9]{3}(\s|-|\.)[0-9]{3}(\s|-|\.)[0-9]{4}')

def PerformSearch(query):
    APIkey = os.getenv("SEARCH_API_KEY")
    searchURL = f"https://serpapi.com/search"

    parameters = {
        'q': query, 
        'api_key': APIkey, 
        'engine': 'google'
    }

    try:
        response = requests.get(searchURL, params = parameters)
        data = response.json()
        return data.get('organic_results', [])

    except Exception as e:
        return {"Error": str(e)}
    

def ExtractFromSearchResults(data):
    extractedData = []
    for result in data:
        snippet = result.get('snippet', "")
        link = result.get('link', "")
        title = result.get('title', "")

        extractedData.append({
            'Title': title,
            'Link': link,
            'Snippet': snippet,})
        
    return extractedData

def ExtractContactFromWebPage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            emails = emailPattern.findall(response.text)
            addresses = addressPattern.findall(response.text)
            phoneNumbers = phonePattern.findall(response.text)

            

            return {
                'Email': emails[0] if emails else "Not found",
                'Address': addresses[0] if emails else "Not found", 
                'Phone': phoneNumbers[0] if phoneNumbers else "Not found"
            }
        else:
            return {'Email': 'Not found', 'Address': 'Not found', 'Phone': 'Not found'}
    except Exception as e:
        print(f"Error in ExtractContactFromWebPage for URL {url}: {e}")
        return {'Email': 'Error', 'Address': 'Error', 'Phone': 'Error'}

def SearchAndExtract(query):
    searchResults = PerformSearch(query)
    extractedData = ExtractFromSearchResults(searchResults)
    for result in extractedData:
        contactInfo = ExtractContactFromWebPage(result['Link'])
        if contactInfo:
            result.update(contactInfo)
    return pd.DataFrame(extractedData)

data = SearchAndExtract("Apple Inc")
print(data)

data.to_csv("AppleSearchResults.csv", index = False)