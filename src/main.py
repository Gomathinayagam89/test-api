from fastapi import FastAPI, HTTPException
import re
import urllib.parse
import requests

app = FastAPI()

# Define a regex pattern that matches any of the restricted characters.
# The restricted characters are: \ / : * ? " < > ; # $ * { } , + = [ ] |
# Note: Some characters are escaped since they have special meanings in regex.
restricted_pattern = re.compile(r'[\\\/:\*\?"<>;#$\{\},\+=\[\]\|]')

@app.get("/generate_url/")
def generate_url(user_input: str):
    # Check if the input contains any restricted characters using regex.
    if restricted_pattern.search(user_input):
        raise HTTPException(status_code=400, detail="Invalid characters in input")

    # Construct the safe URL, encoding the fragment appropriately.
    url = f"https://example.com/foo#{urllib.parse.quote(user_input)}"
    
    requests.get(url)

    return {'status': 'success'}
