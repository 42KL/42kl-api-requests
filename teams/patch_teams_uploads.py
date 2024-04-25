from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import colorama
from colorama import Fore

colorama.init(autoreset=True)

load_dotenv()

# Patching teams uploads means modifying the mark that Moulinette has graded without
# resubmitting the project. As far as we know, this would recalculate the
# final mark of the project, but it does not recalculate the exp of the Cadet.

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

payload = {
	"teams_upload": {
		"final_mark": "125",
		"comment": "basic_tests: GNL OK | bonus_tests: GNL OK"
    }
}

# response = oauth.get(f"{SITE}/v2/teams_uploads/{2150214}")

response = oauth.patch(f"{SITE}/v2/teams_uploads/{1747919}", json=payload)

# print(response.status_code)
# print(response.text)

if (response.status_code == 204):
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color}{response.status_code} {response.text}")