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

# The purpose of this script is to delete accidental scale-teams

# Extract the teams (project submission) of the evaluatee
evaluatee_login = input(f"{Fore.YELLOW}Type in the evaluatee_id: ").lower()

params = {
	"page": {
		"size": 100
	},
	"sort": "-id"
}

response = oauth.get(f"{SITE}/v2/users/{evaluatee_login}/teams", json=params)
if (response.status_code != 200):
	print(f"{Fore.RED}[ ERROR ] - User {evaluatee_login} not found!")
	raise Exception(f"{response.text}")
print(f"{Fore.CYAN}User {evaluatee_login} found!")
teams_data = json.loads(response.text)

# From teams data, extract needed info.
options = []
count = 0

print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'PROJECT': ^15}|{'EVALUATOR': ^15}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+")

for team in teams_data:
	if (team['status'] == 'in_progress' or team['project_gitlab_path'] is None):
		continue
	if count >= 6:
		break
	proj_name = team['project_gitlab_path'].split('/')[-1]
	for scale_teams in team['scale_teams']:
		if (scale_teams['corrector'] == "invisible"):
			continue
		print(f"{Fore.CYAN}|{count: ^7}|{proj_name: ^15}|{scale_teams['corrector']['login']: ^15}|")
		count += 1
		options.append({
			"team_id": team['id'],
			"scale_id": scale_teams['id'],
			"evaluator_id": scale_teams['corrector']['id'],
			"project_name": proj_name,
			"evaluator_login": scale_teams['corrector']['login']
		})

print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+" + '\n')

# Now that the options are parsed, prompt admin for the evaluation session to delete.
choice = int(input(f"{Fore.YELLOW}Type in the index of the scale teams to delete: "))
print(f"{Fore.CYAN}Chosen project {options[choice]['project_name']} with evaluator {options[choice]['evaluator_login']}")

# Confirm and delete
confirm = input(f"{Fore.RED}[ CONFIRMATION ] - Press Enter/Return to delete the above scale teams.")

response = oauth.delete(f"{SITE}/v2/scale_teams/{options[choice]['scale_id']}")
if response.status_code != 204:
	print(f"{Fore.RED}[ ERROR ] - Problem occured when deleting scale-teams with ID {options[choice]['scale_id']}")
	raise Exception(f"{response.text}")
print(f"{Fore.GREEN}Scale teams successfully deleted!")

# Redo eval, get starting time.
time = input(f"{Fore.YELLOW}Type in the starting time of the eval (24hr format, as HH:MM): ")
split_time = [int(i) for i in time.split(":")]
raw_time = dt.now() # + timedelta(minutes=10)
raw_time = raw_time.replace(hour=split_time[0],minute=split_time[1])
raw_time = raw_time - timedelta(hours=8)
parsed_time = raw_time.strftime("%Y-%m-%dT%H:%M:00.000Z")

print(f"{Fore.CYAN}Re-creating evaluation between {evaluatee_login} and {options[choice]['evaluator_login']}")

# Build payload
payload = {
	"scale_teams": [{
		"team_id": options[choice]['team_id'],
		"begin_at": parsed_time,
		"user_id": options[choice]['evaluator_id']
	}]
}

confirm = input(f"{Fore.RED}[ CONFIRMATION ] - Press Enter/Return to schedule an eval for {evaluatee_login}'s {options[choice]['project_name']} with {options[choice]['evaluator_login']}")

# Send POST request
response = oauth.post(f"{SITE}/v2/scale_teams/multiple_create", json=payload)
if response.status_code != 201:
	print(f"{Fore.RED}[ ERROR ] - Problem occured with creating eval session")
	raise Exception(f"{response.text}")
print(f"{Fore.GREEN}Evaluation successfully created!")

# Now, delete one eval point from evaluator, this is so that the nett
# correction points gained/lost is zero. However, feel free to deduct more
# points as punishment.
payload = {
	"reason": "Redo eval session",
	"amount": "-1"
}

response = oauth.post(f"{SITE}/v2/users/{options[choice]['evaluator_login']}/correction_points/add", json=payload)
if response.status_code != 200:
	print(f"{Fore.RED}[ ERROR ] - Problem occured during point subtraction")
	raise Exception(f"{response.text}")
print(f"{Fore.GREEN}Success! The operation has concluded.")