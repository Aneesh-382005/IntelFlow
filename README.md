# AI-Powered Data Extraction Dashboard

## Project Description
This project is an AI-powered dashboard that allows users to upload a dataset (CSV or Google Sheets), run customized web searches, and analyze extracted data using an LLM (Groq) and agents (Langchain). The dashboard allows for seamless integration of search results with your dataset, providing valuable insights in a structured format.

### Key Features:
- The user can upload CSV or Enter a Google Sheets link.
- Performs custom web searches using SerpAPI.
- Use Groq-powered LLM for parsing web results and updating the dataset.
- Automatically create columns for different types of queries.
- Option to download the final CSV file.
  
---

## Setup Instructions
Upload Your Dataset:
Use the file uploader in the dashboard to upload a CSV file or connect to Google Sheets.
Run Search Queries:
Enter your search queries and run them using the integrated search API 
View the Results:
The search results will be displayed in the dashboard
Download the Updated Dataset:
Once the dataset is updated, you can download it as CSV .

### Prerequisites
Ensure that you have Python 3.7+ installed.

Install the necessary dependencies by running the following command:

```bash
pip install -r requirements.txt

``` .env
SERPAPI_API_KEY=your_serpapi_key_here

GROQ_API_KEY=your_groq_api_key_here
```

## Google Sheets Integration Setup

Follow these steps to enable Google Sheets integration using a Google Cloud Service Account:

### Step 1: Enable Google Sheets API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Navigate to **APIs & Services > Library**.
4. Search for "Google Sheets API" and click **Enable**.

### Step 2: Create a Service Account
1. Navigate to **APIs & Services > Credentials**.
2. Click **Create Credentials > Service Account**.
3. Fill in the required details and click **Create and Continue**.
4. Assign the role **Editor** or higher for Google Sheets.
5. Click **Done**.

### Step 3: Download Service Account Key
1. In the **Credentials** tab, find your Service Account.
2. Click the **3-dot menu** on the right and select **Manage keys**.
3. Click **Add Key > Create New Key** and choose **JSON**.
4. Download the JSON file and save it securely (e.g., `service_account.json`).

### Step 4: Share Google Sheet Access
1. Open the Google Sheet you want to access.
2. Click **Share** in the top-right corner.
3. Share the sheet with the Service Account's email address (found in the downloaded JSON file) and give **Editor** access.

### Step 5: Add the JSON Key to Your Project
1. Place the `service_account.json` file in your project directory.
2. Use the file path in your code to authenticate.



# Loom Video : 