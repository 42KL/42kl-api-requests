from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta
import os
import json
import colorama
from colorama import Fore

colorama.init(autoreset=True)

# IMPORTANT: Make sure you have run generate_user_ids.py beforehand

load_dotenv()

# Yay API token stuff
UID = os.getenv("42-UID")
SECRET = os.getenv("42-SECRET")

if UID == None or SECRET == None:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public projects"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Assume that the evaluation scheduling is done by Sunday, so the evaluation date
# should be dt.now() + timedelta(days=1)
start_dt = dt.now() + timedelta(days=1)
final_start = start_dt.strftime("%Y-%m-%dT03:00:00.000Z")

# Try and open user_ids.json to retrieve users.
try:
	with open("user_ids.json", "r") as infile:
		cadet_data = json.load(infile)
except:
	print(f"{Fore.RED}[ ERROR ] - user_ids.json file not found. Please run generate_user_ids.py")
	raise Exception("Necessary file not found!")

# Prompt admin for which Rush to retrieve.
options = [
	["C Piscine Rush 00", "c-piscine-rush-00"],
	["C Piscine Rush 01", "c-piscine-rush-01"],
	["C Piscine Rush 02", "c-piscine-rush-02"]
]

print(f"{Fore.CYAN}0: Rush00\n1: Rush01\n2: Rush02")
choice = int(input(f"{Fore.CYAN}Please type in the index of the Rush: "))
if (choice not in [0, 1, 2]):
	raise Exception("Not a valid option")

# Use a GET /v2/projects/:project_id/teams to receive all the teams who should
# have the status "waiting_for_correction".
project_id = options[choice][1]

params = {
	"page": {
		"size": 100
	},
	"filter": {
		"campus": "34",
		"status": "waiting_for_correction"
	}
}

get_response = oauth.get(f"{SITE}/v2/projects/{project_id}/teams", json=params)

if (get_response.status_code != 200):
	print(f"{Fore.RED}{get_response.status_code} {get_response.text}")
	raise Exception("Error occured on GET request")

teams_data = json.loads(get_response.text)
print(f"{Fore.CYAN}Retrieved {len(teams_data)} teams for {options[choice][0]}")

# Create empty payload.
payload = {
	"scale_teams": []
}

# From the extracted list, go through one by one to extract the team name and id.
# match with an evaluator and add to payload.
# There is a chance that admin will have a typo in the username. It is unwise to
# just exit since there may be alot of teams already entered in the payload.
# Hence, check if it is a typo and then only retrieve from intra.
for team in teams_data:
	while (True):
		evaluator_login = input(f"{Fore.YELLOW}Type in the evaluator for {team['name']}: ").lower()
		try:
			print(f"{Fore.CYAN}Found {evaluator_login} with id {cadet_data[evaluator_login]}")
		except:
			print(f"{Fore.RED}[ WARNING ] - Cadet {evaluator_login} not found!")
			user_input = input(f"{Fore.YELLOW}Type 'Y' if it is a typo: ")
			if (user_input == 'Y'):
				continue
			response = oauth.get(f"{SITE}/v2/users/{evaluator_login}")
			if (response.status_code != 200):
				raise Exception(f"{Fore.RED}[ ERROR ] - User not found")
			temp_data = json.loads(response.text)
			cadet_data[evaluator_login] = temp_data['id']
			print(f"{Fore.CYAN}Found {evaluator_login} with id {cadet_data[evaluator_login]}")
			with open("user_ids.json", "w") as outfile:
				json.dump(cadet_data, outfile, indent=4)
		evaluator_id = cadet_data[evaluator_login]
		break
	node = {
		"team_id": team['id'],
		"begin_at": final_start,
		"user_id": evaluator_id
	}
	payload["scale_teams"].append(node)

# Save the payload for visual checkup
print(f"{Fore.CYAN}Team entry done, saving payload as payload.json...")
with open("payload.json", "w") as outfile:
	json.dump(payload, outfile, indent=4)
print(f"{Fore.CYAN}Done!")

confirmed = input(f"{Fore.RED}[ CONFIRMATION ] - Press Enter to confirm payload")

response = oauth.post(f"{SITE}/v2/scale_teams/multiple_create", json=payload)

if response.status_code == 201:
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color} {response.status_code} {response.text}")