import json
import pandas as pd

def CleanedResponse(llmResponse):
    cleanedResponse = llmResponse.split(']')[0] + ']'

    try:
        parsedData = json.loads(cleanedResponse)

        df = pd.DataFrame(parsedData)

        return df

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    
