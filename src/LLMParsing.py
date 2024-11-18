from langchain_core.prompts import PromptTemplate
#from langchain.chains import 
from langchain_groq import ChatGroq
import os
from groq import Groq
import json
from WebSearchForLLM import GetInsights

groqLLM = os.getenv("GROQ_API_KEY")

model = ChatGroq(model = "llama-3.1-70b-versatile", api_key = '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')

def PassPrompt(userPrompt):
    messages = [
        (
            "system",
            """You are an AI assistant. Your task is to extract the company name and the specific information the user is asking for from the prompt.
            Extracted Information:
        - Company: [The company name]
        - Queries: [List of specific information requested, separated by commas]
        """,
        ),
        ("human", userPrompt),
    ]

    response = model.invoke(messages)

    structuredResponse = response.content

    return structuredResponse

def ProcessUserPrompt(userPrompt):
    structuredResponse = PassPrompt(userPrompt)
    line = structuredResponse.split("\n")
    company = line[1].split(":")[1].strip()
    queries = [q.strip() for q in line[2].split(":")[1].split(",")]

    return company, queries
    

def ProcessUserPromptAndGoogleSearch(userPrompt):
    company, queries = ProcessUserPrompt(userPrompt)
    insights = GetInsights(company, queries)
    return insights

#print(ProcessUserPromptAndGoogleSearch("Gimme the phone and email of Google"))


def ParseSearchResults(userPrompt, insights):
    messages = [
        (
            "system",
            """
            You are an intelligent extraction assistant. You will be provided with search results for a specific company and query. Your task is to extract the most relevant information directly addressing the query, using the snippet and title provided.

            ### Input Data Format:
            [
            {
                "company": "Company Name",
                "query": "Query",
                "Title": "Search result title",
                "Link": "Search result URL",
                "Snippet": "Search result snippet"
            },
            ...
            ]

            ### Task:
            1. Focus on the query and extract the most relevant information directly answering it.
            - For example, if the query is "email address," return the extracted email(s).
            - If the query is "CEO name," return the CEO's name if found.
            - If the query is "headquarters location," return the location if found.
            2. If the requested information is not found in the snippets or titles, return "Not found."
            3. Use only the information from the provided snippets and titles. Do not generate data not present in the input.

            ### Output Format:
            ```json
            {
            "company": "Company Name",
            "query": "Query",
            "result": "Extracted result or 'Not found'"
            }
            """,), 
            ("human", f"{userPrompt} \n\n {insights}"),
        ]
    
    response = model.invoke(messages)
    return response.content


def LLMFunction(userPrompt):
    insights = ProcessUserPromptAndGoogleSearch(userPrompt)
    return ParseSearchResults(userPrompt, insights)

print(LLMFunction("Director of Thapar Institute of Engineering and Technology"))
