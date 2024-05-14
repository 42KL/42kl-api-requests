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
SCOPE = "public projects"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Prompt admin for evaluator, use that to find the ID.
# For this we will use GET /v2/users/:id
evaluator = input(f"{Fore.YELLOW}Type in the intra id of the evaluator: ").lower()

get_evaluator_req = oauth.get(f"{SITE}/v2/users/{evaluator}")
if (get_evaluator_req.status_code == 200):
	print(f"{Fore.GREEN}User {evaluator} found!")
else:
	print(f"{Fore.RED}User {evaluator} is not found!")
	raise (Exception("User with intra ID is not found."))

evaluator_data = json.loads(get_evaluator_req.text)
evaluator_id = evaluator_data["id"]
# print(f"{Fore.CYAN}User {evaluator} has id {evaluator_id}")

# Prompt admin for evaluatee, then use that to find the team_id.
# For this we will use GET /v2/users/:user_id/teams.
evaluatee = input(f"{Fore.YELLOW}Type in the intra id of the evaluatee: ").lower()

params = {
	"page": {
		"size": 10
	},
	"sort": "-id"
}

get_evaluatee_req = oauth.get(f"{SITE}/v2/users/{evaluatee}/teams", json=params)
if (get_evaluatee_req.status_code == 200):
	print(f"{Fore.GREEN}User {evaluatee} found!")
else:
	print(f"{Fore.RED}User {evaluatee} is not found!")
	raise (Exception("User with intra ID is not found."))

# From the list, return a list of the projects that are waiting for correction
# and create an options array.
evaluatee_teams_data = json.loads(get_evaluatee_req.text)
options = []
count = 0

print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'PROJECT': ^15}|{'TEAM_ID': ^15}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+")

for item in evaluatee_teams_data:
	if item['status'] != "waiting_for_correction" or item["project_gitlab_path"] is None:
		continue
	proj_name = item["project_gitlab_path"].split('/')[-1]
	print(f"{Fore.CYAN}|{count: ^7}|{proj_name: ^15}|{item['id']: ^15}|")
	options.append([proj_name, item['id']])
	count += 1

print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+" + '\n')

# If there are no projects with the right status, exit prog.
# Else if there is only one project, proceed with default option.
# Else, ask admin which project to set an eval for.
if count == 0:
	print(f"{Fore.RED}[ ERROR ]: User {evaluatee} does not have any projects to evaluate!")
	raise (Exception("No projects to evaluate."))
else:
	choice = input(f"{Fore.YELLOW}Type in the index of the project to set an evaluation (Default is {0}): ")
	if choice == "":
		choice = 0
	else:
		choice = int(choice)

print(f"{Fore.CYAN}Chosen {evaluatee}'s {options[choice][0]} with id {options[choice][1]}")
team_id = options[choice][1]

# Get the starting time for the evaluation. Get the time in Malaysian time and correct to Paris time.
# Paris time = Malaysia Time - 8 hours
raw_date = input(f"{Fore.YELLOW}Type in the date of the eval in the format DD/MM/YYYY (Default is today): ")
if raw_date == "":
	raw_date = dt.now().strftime("%d/%m/%Y")

raw_time = input(f"{Fore.YELLOW}Type in the start time of the eval in HH:MM (24h format): ")

raw_start = f"{raw_date} {raw_time}"
parsed_start = dt.strptime(raw_start, "%d/%m/%Y %H:%M")
parsed_start = parsed_start - timedelta(hours=8)

final_start = parsed_start.strftime("%Y-%m-%dT%H:%M:00.000Z")

# Confirmation
print(f"{Fore.CYAN}\nSimulated payload - Check for final details")
print(f"{Fore.CYAN}team_id : {team_id}")
print(f"{Fore.CYAN}user_id : {evaluator_id}")
print(f"{Fore.CYAN}begin at : {final_start}")
input(f"{Fore.RED}[ Confirmation ] - Press enter to confirm")

# Build payload
payload = {
	"scale_teams" : [{
		"team_id": team_id,
		"begin_at": final_start,
		"user_id": evaluator_id
	}]
}

# Make the request
response = oauth.post(f"{SITE}/v2/scale_teams/multiple_create", json=payload)

if response.status_code == 201:
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color} {response.status_code} {response.text}")