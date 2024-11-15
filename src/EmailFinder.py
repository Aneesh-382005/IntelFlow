import requests
import re
import time
import csv
from dotenv import load_dotenv
import os

load_dotenv()
APIkey = os.getenv("SEARCH_API_KEY")

def SearchEmails(companyName):
    search_query = f"{companyName} contact us"
    params = {
        "engine": "google",
        "q": search_query,
        "api_key": APIkey,
        "num": 20
    }
    response = requests.get("https://serpapi.com/search", params=params)
    
    if response.status_code == 200:
        return response.json().get("organic_results", [])
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []
    
def ExtractEmails(text):
    emailPattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    return re.findall(emailPattern, text)

def ExtractAddress(text):
    addressPattern = re.compile(r'\d{1,5}\s[\w\s]+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Way|Square|Sq)\b')
    return re.findall(addressPattern, text)

def ExtractPhoneNumbers(text):
    phonePattern = re.compile(r'(\(?\+?[0-9]*\)?)?(\s|-|\.)?[0-9]{3}(\s|-|\.)[0-9]{3}(\s|-|\.)[0-9]{4}')
    return re.findall(phonePattern, text)

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

def FindCompanyEmails(companyName):
    results = SearchEmails(companyName)
    emails = []
    
    for result in results:

        snippetEmails = ExtractEmails(result.get("snippet", ""))
        titleEmails = ExtractEmails(result.get("title", ""))
        linkEmmails = ExtractEmails(result.get("link", ""))
        
        for email in set(snippetEmails + titleEmails + linkEmmails):
            emails.append({
                "company": companyName,
                "email": email,
                "source": result.get("link", "")
            })
    
    return emails

def SaveEmailsToCSV(emails, filename="CompanyEmails.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["company", "email", "source"])
        writer.writeheader()
        writer.writerows(emails)
    print(f"Emails saved to {filename}")


def CompanyToCSV(companyName):
    emails = FindCompanyEmails(companyName)
    SaveEmailsToCSV(emails)
    time.sleep(5)


CompanyToCSV("Google")
