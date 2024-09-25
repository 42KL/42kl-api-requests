from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import colorama
import json
from colorama import Fore

colorama.init(autoreset=True)

load_dotenv()

# Yay API token stuff
UID = os.getenv("42-UID")
SECRET = os.getenv("42-SECRET")

if UID == None or SECRET == None:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Get feedbacks from a particular user and see what pops out.
# OBJECTIVE - Is it possible to track event feedbacks?

# Setup params
params = {
	"page": {
		"size": 100
	},
	"filter": {
		"user_id": 172816
	},
	"sort": "-id"
}

# Make GET request
response = oauth.get(f"{SITE}/v2/feedbacks", json=params)

if response.status_code != 200:
	print(response.status_code)
	print(response.text)
	raise Exception(f"KABOOM")

data = json.loads(response.text)

with open(f"feedbacks.json", "w") as fd:
	json.dump(data, fd, indent=4)