import pandas as pd
import requests
from dotenv import load_dotenv
import os
import re
from WebSearch import ExtractContactFromWebPage

load_dotenv()

emailPattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
addressPattern = re.compile(r'\d{1,5}\s[\w\s]+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Way|Square|Sq)\b')
phonePattern = re.compile(r'(\(?\+?[0-9]*\)?)?(\s|-|\.)?[0-9]{3}(\s|-|\.)[0-9]{3}(\s|-|\.)[0-9]{4}')

def PerformSearch(query, targetSite = "linkedin.com"):
    APIkey = os.getenv("SEARCH_API_KEY")
    searchURL = f"https://serpapi.com/search"

    if targetSite:
        query = f"site:{targetSite} {query}"

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
        emails = emailPattern.findall(snippet)
        addresses = addressPattern.findall(snippet)
        PhoneNumbers = phonePattern.findall(snippet)


        extractedData.append({
            'Title': title,
            'Link': link,
            'Snippet': snippet,
            'Email': emails[0] if emails else "Not found",
            'Address': addresses[0] if emails else "Not found", 
            'Phone': PhoneNumbers[0] if PhoneNumbers else "Not found"})
        
    return extractedData

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