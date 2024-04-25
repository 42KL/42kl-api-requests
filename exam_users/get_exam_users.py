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

# Get ID of the exam from running the script exams > get_exams.py
exam_id = 17844

response = oauth.get(f"{SITE}/v2/exams/{exam_id}/exams_users")

if response.status_code == 200:
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color} {response.status_code} {response.text}")

data = json.loads(response.text)

with open(f"exam_users_for_{exam_id}.json", "w") as outfile:
	json.dump(data, outfile, indent=4)