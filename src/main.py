from fastapi import FastAPI, HTTPException
import re
import urllib.parse
import requests

app = FastAPI()

# Define a regex pattern for restricted characters.
# Restricted characters: \ / : * ? " < > ; # $ * { } , + = [ ]
restricted_pattern = re.compile(r'[\\\/:\*\?"<>;#$\{\},\+=\[\]]')

@app.get("/generate_url/")
def generate_url(user_input: str):
    # Validate: Reject input if any restricted characters are found.
    if restricted_pattern.search(user_input):
        raise HTTPException(status_code=400, detail="Invalid characters in input")
    
    # URL-encode the input to safely insert into the URL path.
    safe_user_input = urllib.parse.quote(user_input, safe='')
    
    # Build URL components.
    scheme = "https"
    netloc = "example.com"  # Fixed host
    path = f"/foo/{safe_user_input}"
    
    # Assemble the URL using urlunparse.
    url = urllib.parse.urlunparse((scheme, netloc, path, "", "", ""))
    
    # For documentation and to ease CodeQL analysis, add a comment:
    # Note: The dynamic data only affects the path portion of the URL.
    # The scheme and host (netloc) are constant, so the risk of SSRF is minimized.
    response = requests.get(url)
    
    return {
        'status': 'success',
        'requested_url': url,
        'response_status': response.status_code
    }
