from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import json
import os
import colorama
from colorama import Fore

colorama.init(autoreset=True)
load_dotenv()

# This script aims to get the project_user id for a Cadet, and use that
# id to allow them to retry the project without having to go through the
# intra GUI.

# Testing shows that the endpoint automatically registers the user for the
# project again, so the user does not have to manually click the "Retry"
# button on the intra GUI.

UID = os.getenv("42-UID")  # EDIT .env file
SECRET = os.getenv("42-SECRET")  # EDIT .env file

if UID == None:
    raise (Exception("UID not defined, edit .env file"))
if SECRET == None:
    raise (Exception("SECRET not defined, edit .env file"))

SITE = "https://api.intra.42.fr"
SCOPE = "public projects"

# Create a client using the OAuth2Session with a BackendApplicationClient
client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

# Fetch the token using client_credentials flow
token = oauth.fetch_token(
    token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Retrieve project_users and list them.
target_login = input(f"{Fore.YELLOW}Type in the Cadet's login: ")
payload = {
    "filter": {
        "status": "finished"
    }
}

requests = oauth.get(f"{SITE}/v2/users/{target_login}/projects_users", json=payload)
if requests.status_code != 200:
    raise Exception(f"{Fore.RED}[ ERROR ] Request failed with status code {requests.status_code}\n{requests.text}")
else:
    print(f"{Fore.GREEN}User {target_login} found!")

project_users_data = json.loads(requests.text)
requests.close()
options = []
count = 0

print(f"{Fore.CYAN}+{'':-^7}+{'':-^30}+{'':-^20}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'PROJECT NAME': ^30}|{'FINAL MARK': ^20}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^30}+{'':-^20}+")

for item in project_users_data:
    # list latest 5 projects, increase if needed
    if count == 5:
        break
    project_name = item["project"]["name"]
    final_mark = str(item["final_mark"])
    project_user_id = item["id"]
    options.append([project_name, final_mark, project_user_id])
    print(f"{Fore.CYAN}|{count: ^7}|{project_name: ^30}|{final_mark: ^20}|")
    count += 1

print(f"{Fore.CYAN}+{'':-^7}+{'':-^30}+{'':-^20}+")

choice = input(f"{Fore.YELLOW}Type in the index of the project to allow retry (default is 0): ")
if choice == "":
    choice = 0
elif not choice.isdigit() or int(choice) < 0 or int(choice) >= len(options):
    raise Exception(f"{Fore.RED}[ ERROR ] Invalid choice. Please enter a valid index.")
else:
    choice = int(choice)

print(f"{Fore.CYAN}Chosen {target_login}'s {options[choice][0]} with id {options[choice][2]} to allow retry.")
input(f"{Fore.YELLOW}[ CONFIRMATION ] Press Enter to continue or Ctrl+C to cancel...")

print(f"{Fore.YELLOW}[ INFO ] Sending request to allow retry for project user {options[choice][2]}...")

chosen_project_user_id = options[choice][2]

request = oauth.put(f"{SITE}/v2/projects_users/{chosen_project_user_id}/retry", json={"force":"true"})
if request.status_code != 204:
    raise Exception(f"{Fore.RED}[ ERROR ] Request failed with status code {request.status_code}\n{request.text}")
else:
    print(f"{Fore.GREEN}[ SUCCESS ] Project user {chosen_project_user_id} has been allowed to retry.")