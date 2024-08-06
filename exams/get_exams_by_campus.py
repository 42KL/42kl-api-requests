from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import colorama
from colorama import Fore
import json

colorama.init(autoreset=True)

load_dotenv()

UID = os.getenv("42-UID")
SECRET = os.getenv("42-SECRET")
CAMPUS_ID = os.getenv("42-CAMPUS")

if None in [UID, SECRET, CAMPUS_ID]:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

response = oauth.get(f"{SITE}/v2/campus/{CAMPUS_ID}/exams")

color = Fore.GREEN
if int(response.status_code) != 200:
	color = Fore.RED
print(f"{color} {response.status_code}")

data = json.loads(response.text)

# print(data)

json_obj = json.dumps(data, indent=4)

with open("exams_of_campus_34.json", "w") as outfile:
	outfile.write(json_obj)