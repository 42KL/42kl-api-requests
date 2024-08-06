# The purpose of this script is to get all Cadets of 42KL,
# together with their user IDs. This list will be saved as
# a json file, in the order of "login": "user_id" key pairs.

# This is so that I can use that same list in order to arrange RUSH
# evals, without needing to GET every single evaluator every single time.

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

# We will be using the GET /v2/cursus/:cursus_id/cursus_users API, but also
# with some parameters in order to get ALL Cadets (page is limited to 100 entries)
# and also narrow down the search.

page_no = 1
page_size = 100
dict_data = {}

while page_size == 100:
	params = {
		"page": {
			"number": page_no,
			"size": 100
        },
		"filter": {
			"campus_id": f"{CAMPUS_ID}",
			"active": "true"
		}
    }
	response = oauth.get(f"{SITE}/v2/cursus/42cursus/cursus_users", json=params)
	if response.status_code != 200:
		raise Exception(f"{Fore.RED}Problem while getting all Cadets")
	temp_data = json.loads(response.text)
	page_size = len(temp_data)
	page_no += 1

	for item in temp_data:
		dict_data[item['user']['login']] = item['user']['id']

with open("user_ids.json", "w") as outfile:
	json.dump(dict_data, outfile, indent=4)