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
SCOPE = "public projects"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# user_id = 172791
user_id = "habdulla"

params = {
	"page": {
		"size": 20
    }
}

response = oauth.get(f"{SITE}/v2/users/{user_id}/teams_users", json=params)

# Print response status and content
if (response.status_code == 200):
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color} {response.status_code}")

# Below is just testing to see how to use the returned response.

data = json.loads(response.text)
total = len(data)

print("Items:\n")
count = 0

# From the response, extract the 5 most recent submitted projects (status is finished)
# that are not exams (if exam then project_gitlab_path is None), and display the project
# gitlab path and final mark.
for item in data:
	if count == 5:
		break
	if item["team"]["status"] != "finished" or item['team']['project_gitlab_path'] is None:
		continue
	else:
		print(f"[{count}] : {item['team']['project_gitlab_path']} with {item['team']['final_mark']}%")
	count += 1

json_obj = json.dumps(data, indent=4)
with open(f"teams_of_{user_id}.json", "w") as outfile:
	outfile.write(json_obj)