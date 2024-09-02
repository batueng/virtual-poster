import requests
import json

with open("access_token.json", "r") as f:
    j = json.load(f)
    access_token = j["access_token"]
    refresh_token = j["refresh_token"]

endpoint = "https://api.spotify.com/v1/me/player"

# Make the API request with the access token
response = requests.get(endpoint, headers={
    "Authorization": f"Bearer {access_token}"
})

# Check if the response is successful
if response.status_code == 200:
    j = response.json()
    print(j["item"]["album"]["images"][0]["url"])
    #["item"]["album"]["images"]["url"]
else:
    print(f"Error: {response.status_code} - {response.text}")
