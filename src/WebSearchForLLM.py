import csv
import time
from dotenv import load_dotenv
import pandas as pd 
import os
import requests

load_dotenv()
APIkey = os.getenv("SEARCH_API_KEY")

def GetInsights(company, queries, APIkey=APIkey):
    insights = []
    for query in queries:
        params = {
            "engine": "google",
            "q": f"{company} {query}",
            "api_key": APIkey,
            "num": 20
        }
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code == 200:
            organic_results = response.json().get("organic_results", [])
            for result in organic_results:
                insights.append({
                    "company": company,
                    "query": query,
                    "Title": result.get("title", "N/A"),
                    "Link": result.get("link", "N/A"),
                    "Snippet": result.get("snippet", "N/A")
                })
        else:
            print(f"Failed to fetch data for {company} with query '{query}': {response.status_code}")
    return insights

