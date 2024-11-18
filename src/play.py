"""
def parse_structured_response(response_content):
    
    # Split the content into lines
    lines = response_content.split("\n")
    
    # Extract the company name
    company_line = lines[]  # Second line contains the company information
    company = company_line.split(":")[1].strip()  # Extract and clean
    
    # Extract the queries
    queries_line = lines[2]  # Third line contains the queries
    queries = [q.strip() for q in queries_line.split(":")[1].split(",")]  # Split and clean
    
    # Return parsed information
    return {
        "company": company,
        "queries": queries
    }
"""


# Example usage
structured_response = """
Extracted Information:
- Company: Google
- Queries: phone number, email address
"""


lines = structured_response.split("\n")

print(lines[2].split(":")[1].strip())
queries = [q.strip() for q in lines[3].split(":")[1].split(",")]
print(queries)