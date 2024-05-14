from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import colorama
import json
from colorama import Fore

colorama.init(autoreset=True)

load_dotenv()

# Just run the script, all inputs are prompted.

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

# Due to how the API call is, it is necessary to use a GET request for the teams_id of the
# affected Cadet/Pisciner. We will use the one that is documented under "GET /v2/users/:user_id/teams"
# in the 42 API Official Documentation.

# Get the teams (details of all submitted and current projects) of the user.
user_id = input(f"{Fore.YELLOW}Type in the user: ").lower()

params = {
	"page": {
		"size": 20
	},
	"sort": "-id"
}
get_response = oauth.get(f"{SITE}/v2/users/{user_id}/teams", json=params)

if (get_response.status_code == 200):
	print(f"{Fore.GREEN}User {user_id} found!" + '\n')
else:
	print(f"{Fore.RED}User {user_id} is not found!")
	raise (Exception("User with intra ID is not found."))

# From the list, take the 5 most recent submitted and Momo-graded projects that are not exams
# and create an options array for which one to reset

data = json.loads(get_response.text)
count = 0
options = []
default_option = -1

print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+{'':-^7}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'PROJECT': ^15}|{'TEAM_ID': ^15}|{'NORME': ^7}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+{'':-^7}+")

for item in data:
	if count == 5:
		break
	if item['status'] != 'finished' or item['project_gitlab_path'] is None or len(item['teams_uploads']) == 0:
		continue
	proj_name = item['project_gitlab_path'].split('/')[-1]
	norme_count = len([1 for x in item['teams_uploads'][0]['comment'].split('|') if "Norme" in x or "Norm" in x])
	if (norme_count > 0):
		print(f"{Fore.RED}|{count: ^7}|{proj_name: ^15}|{item['id']: ^15}|{norme_count: ^7}|")
		if default_option == -1:
			default_option = count
	else:
		print(f"{Fore.CYAN}|{count: ^7}|{proj_name: ^15}|{item['id']: ^15}|{norme_count: ^7}|")
	options.append([proj_name, item['id']])
	count += 1

print(f"{Fore.CYAN}+{'':-^7}+{'':-^15}+{'':-^15}+{'':-^7}+" + '\n')

# Decide which option to be parsed into the payload of the POST request.
if (default_option != -1):
	choice = input(f"{Fore.YELLOW}Type in the index of the project to resubmit (Default is {default_option}): ")
	if choice == "":
		choice = default_option
	else:
		choice = int(choice)
else:
	choice = int(input(f"{Fore.YELLOW}Type in the index of the project to resubmit: "))

# Confirm payload before sending
confirmed = input(f"{Fore.RED}[ CONFIRMATION ] - Press Enter to reset {user_id}'s {options[choice][0]} with id {options[choice][1]} ?")

response = oauth.post(f"{SITE}/v2/teams/{options[choice][1]}/reset_team_uploads")

if (response.status_code == 200):
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color} {response.text}")