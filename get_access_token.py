import requests
import string
import random
import json
from urllib.parse import urlencode
from flask import Flask, redirect, Response, request, jsonify
import base64

app = Flask(__name__)

# Set up your variables
f = open("client.json", "r")
j = json.loads(f.read())

client_id = j["client_id"]
client_secret = j["client_secret"]
redirect_uri = 'http://localhost:8888/callback'
scope = 'user-read-playback-state'

def generate_random_string(length=16):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/login')
def login():
    state = generate_random_string()
    
    # Construct the authorization URL
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    })
    
    # Redirect to the authorization URL
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state is None:
        return redirect('/#error=state_mismatch')

    # Prepare the headers and form data for the token request
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    # Make the POST request to exchange the authorization code for an access token
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    # Parse the JSON response
    token_info = response.json()
    f = open("access_token.json", "w+")
    f.write(json.dumps(token_info, indent=4))
    # You can now use the access token in further API requests
    # For demonstration, we'll just return the token info as JSON
    return jsonify(token_info)

if __name__ == '__main__':
    app.run(port=8888)