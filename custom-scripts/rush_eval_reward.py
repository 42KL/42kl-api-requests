from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from time import sleep
import os
import json
import colorama
from colorama import Fore

colorama.init(autoreset=True)

# IMPORTANT: Make sure you have run generate_user_ids.py beforehand

load_dotenv(override=True)

# Yay API token stuff
UID = os.getenv("42-UID")
SECRET = os.getenv("42-SECRET")
CAMPUS_ID = os.getenv("42-CAMPUS")

if None in [UID, SECRET, CAMPUS_ID]:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public projects"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# First, check if there is a payload.json file which is generated after the script
# create_rush_evals.py has been run.
try:
	with open("payload.json", "r") as fd:
		eval_data = json.load(fd)
except Exception as err:
	print(f"{Fore.RED}The required payload.json file is not found. Ensure that create_rush_evals.py has already been run.")
	exit(1)

# prep payload.
payload = {
	"reason": "Rush evals",
	"amount": "1"
}

# Iterate through the eval_data and extract just the user_id. This is the Cadet to be
# given an eval point.
success = 0
failed = 0
print(f"{Fore.CYAN}Beginning process...\n")
for data in eval_data['scale_teams']:
	response = oauth.post(f"{SITE}/v2/users/{data['user_id']}/correction_points/add", json=payload)
	if response.status_code != 200:
		print(f"{Fore.RED}Failed for user_id {data['user_id']}")
		failed += 1
	else:
		success_data = json.loads(response.text)
		print(f"{Fore.GREEN}Succeeded for {success_data['login']}")
		success += 1
	sleep(0.5)

print(f"\n{Fore.CYAN}Process comepleted.\n{Fore.GREEN}Succeeded: {success}\n{Fore.RED}Failed: {failed}")