import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os

load_dotenv()

UID = os.getenv("42-UID")  # EDIT .env file
SECRET = os.getenv("42-SECRET")  # EDIT .env file
CAMPUS_ID = os.getenv("42-CAMPUS")

if None in [UID, SECRET, CAMPUS_ID]:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public projects"

# Create a client using the OAuth2Session with a BackendApplicationClient
client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

# Fetch the token using client_credentials flow
token = oauth.fetch_token(
    token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Make a request
photo_links = []
i = 1
while True:
    response = oauth.get(
        f"{SITE}/v2/users?filter[primary_campus_id]={CAMPUS_ID}&per_page=100&page={i}"
    )

    response_json = response.json()
    for user in response_json:
        if (user["image"]["link"] == None):
            continue
        photo_links.append(user["image"]["link"])
        print(user["login"], user["image"]["link"])
    if len(response_json) != 100:
        break
    i += 1
with open("users_pictures_links.txt", "w") as f:
    for link in photo_links:
        f.write(link + "\n")
# Print response status and content
print(response.status_code)
print(response.text)
