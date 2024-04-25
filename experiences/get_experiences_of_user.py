from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import colorama
from colorama import Fore
import json

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

# Using a user_id, receive a list of exp received per submission.
user_id = "zyeoh"

params = {
	"page": {
		"size": 100
    }
}

response = oauth.get(f"{SITE}/v2/users/{user_id}/experiences")

if response.status_code == 200:
	color = Fore.GREEN
else:
	color = Fore.RED

print(f"{color}{response.status_code}")

data = json.loads(response.text)

with open("new_test.json", "w") as outfile:
	json.dump(data, outfile, indent=4)