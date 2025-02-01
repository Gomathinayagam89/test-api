from fastapi import FastAPI, HTTPException
import re
import urllib.parse
import requests

app = FastAPI()

# Define a regex pattern that matches any of the restricted characters.
restricted_pattern = re.compile(r'[\\\/:\*\?"<>;#$\{\},\+=\[\]\|]')

@app.get("/generate_url/")
def generate_url(user_input: str):
    # Check if the input contains any restricted characters.
    if restricted_pattern.search(user_input):
        raise HTTPException(status_code=400, detail="Invalid characters in input")

    # Prepare the base URL parts.
    scheme = "https"
    netloc = "example.com"
    path = "/foo"
    params = ""
    query = ""
    # Only the fragment comes from user input, and fragments are not sent over HTTP.
    fragment = urllib.parse.quote(user_input)

    # Reassemble the URL.
    url = urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))

    # Make the request.
    requests.get(url)

    return {'status': 'success'}
