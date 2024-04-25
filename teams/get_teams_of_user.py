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

# user_id = 172791
user_id = "tcadet"

# Load 30 "items" in one page.
params = {
	"page": {
		"size": 100
    }
}

response = oauth.get(f"{SITE}/v2/users/{user_id}/teams", json=params)

# Print response status and content
if (response.status_code == 200):
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color} {response.status_code}")


# Code below are for testing purposes

# Load response into a JSON array and reverse it to arrange the project list from
# most recent to least recent.
data = json.loads(response.text)
# data = data[::-1]

# From the reversed list, take the 5 most recent submitted and Momo-graded projects that are not exams
# and get the project name (project_gitlab_path), id, and Momo's comment to check for Norme anomalies (teams_uploads)

# count = 0
# for item in data:
# 	if count == 5:
# 		break
# 	if item['status'] != 'finished' or item['project_gitlab_path'] is None or len(item['teams_uploads']) == 0:
# 		continue
# 	proj_name = str(item['project_gitlab_path']).split('/')[-1]
# 	norme_count = len([1 for x in item['teams_uploads'][0]['comment'].split('|') if 'Norme' in x])
# 	print(f"[{count}] : {proj_name} | {item['id']} | {norme_count}")
# 	count += 1

# json_obj = json.dumps(data, indent=4)
# with open(f"teams_of_{user_id}.json", "w") as outfile:
# 	outfile.write(json_obj)

with open("new_test.json", "w") as outfile:
	json.dump(data, outfile, indent=4)