from fastapi import FastAPI, HTTPException
import re
import urllib.parse
import requests

app = FastAPI()

# Define a regex pattern for the restricted characters.
# The characters are: \ / : * ? " < > ; # $ * { } , + = [ ]
# Note: The '*' appears twice; only one occurrence is necessary.
restricted_pattern = re.compile(r'[\\\/:\*\?"<>;#$\{\},\+=\[\]]')

@app.get("/generate_url/")
def generate_url(user_input: str):
    # Validate: Reject input if any restricted characters are found.
    if restricted_pattern.search(user_input):
        raise HTTPException(status_code=400, detail="Invalid characters in input")

    # URL-encode the input so it safely becomes part of the path.
    # The safe parameter is set to an empty string to force encoding of all characters.
    safe_user_input = urllib.parse.quote(user_input, safe='')

    # Construct the URL by inserting the encoded input into the path.
    url = f"https://example.com/foo/{safe_user_input}"

    # Make the HTTP request.
    response = requests.get(url)

    return {'status': 'success', 'requested_url': url, 'response_status': response.status_code}
