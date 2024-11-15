import requests
import re
import time
import csv
from dotenv import load_dotenv
import os

load_dotenv()
APIkey = os.getenv("SEARCH_API_KEY")

emailPattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
addressPattern = re.compile(r'\d{1,5}\s[\w\s]+(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Way|Square|Sq)\b')
phonePattern = re.compile(r'(\(?\+?[0-9]*\)?)?(\s|-|\.)?[0-9]{3}(\s|-|\.)[0-9]{3}(\s|-|\.)[0-9]{4}')

def SearchResults(companyName, searchQuery=None):
    searchQuery = f"{companyName} {searchQuery}"
    params = {
        "engine": "google",
        "q": searchQuery,
        "api_key": APIkey,
        "num": 20
    }
    response = requests.get("https://serpapi.com/search", params=params)
    
    if response.status_code == 200:
        return response.json().get("organic_results", [])
    else:
        print(f"Failed to fetch data for {companyName} with query '{searchQuery}': {response.status_code}")
        return []

def ExtractEmails(text):
    return re.findall(emailPattern, text)

def ExtractAddresses(text):
    return re.findall(addressPattern, text)

def ExtractPhoneNumbers(text):
    return ["".join(num) for num in re.findall(phonePattern, text)]

def ProcessResults(results, queryType):
    extractedData = []
    for result in results:
        snippet = result.get("snippet", "")
        title = result.get("title", "")
        link = result.get("link", "")
        text = snippet + " " + title

        if queryType == "email":
            data = ExtractEmails(text)
        elif queryType == "address":
            data = ExtractAddresses(text)
        elif queryType == "phone":
            data = ExtractPhoneNumbers(text)
        else:
            data = text 

        for item in set(data):
            extractedData.append({
                "queryType": queryType,
                "data": item,
                "source": link
            })

    return extractedData

def SearchCompaniesWithQueries(companies, queries):
    allResults = []
    for company in companies:
        for query in queries:
            print(f"Searching for {query} for {company}")
            results = SearchResults(company, query)
            extractedData = ProcessResults(results, query)
            for data in extractedData:
                allResults.append({
                    "company": company,
                    "query": query,
                    "queryType": data["queryType"],
                    "data": data["data"],
                    "source": data["source"],
                })
            time.sleep(2)
    return allResults


def SaveToCSV(data, filename = "SearchResults.csv"):
    with open(filename, mode = "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["company", "query", "queryType", "data", "source"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Search Results saved to {filename}")


def PerformWebSearch (companies, queries):
    results = SearchCompaniesWithQueries(companies, queries)
    SaveToCSV(results)

companies = ["Google", "Facebook", "Microsoft"]
queries = ["email", "address", "phone"]
PerformWebSearch(companies, queries)
