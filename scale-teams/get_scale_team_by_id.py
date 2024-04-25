from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta
import os
import json
import colorama
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

# Get ID of the scale teams from running the script get_teams_of_user.py
# Each evaluation session will have their own scale_teams_id.
scale_teams_id = 6621457

response = oauth.get(f"{SITE}/v2/scale_teams/{scale_teams_id}")

if response.status_code == 200:
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color} {response.status_code} {response.text}")

data = json.loads(response.text)

with open(f"scale_teams.json", "w") as outfile:
	json.dump(data, outfile, indent=4)