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
SCOPE = "public"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Get the ID of the user using a simple GET
intra_id = input(f"{Fore.YELLOW}Type in the intra id of the user: ").lower()

get_student_id = oauth.get(f"{SITE}/v2/users/{intra_id}")
if (get_student_id.status_code == 200):
	print(f"{Fore.GREEN}User {intra_id} found!")
else:
	print(f"{Fore.RED}User {intra_id} is not found!")
	raise (Exception("User with intra ID is not found."))

student_data = json.loads(get_student_id.text)
student_id = student_data["id"]

# Get the ID of the previous 5 exams using GET /v2/campus/:campus_id/exams
# From there, allow admin to choose which one to register the user for.
get_exam_req = oauth.get(f"{SITE}/v2/campus/34/exams")

if (get_exam_req.status_code != 200):
	raise Exception("Error on GET request for /v2/campus/:campus_id/exams")

exam_data = json.loads(get_exam_req.text)
count = 0
options = []

print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'ID': ^9}|{'NAME': ^35}|{'DATE': ^12}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+")

for item in exam_data:
	if count == 5:
		break
	exam_start = item['begin_at'].split('T')[0]
	print(f"{Fore.CYAN}|{count: ^7}|{item['id']: ^9}|{item['name']: ^35}|{exam_start: ^12}|")
	options.append([item['id'], item['name'], exam_start])
	count += 1


print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+")

exam_choice = int(input(f"{Fore.YELLOW}Type in the index of the exam to add the student into: "))
print(f"{Fore.CYAN}Chosen {options[exam_choice][1]} that starts on {options[exam_choice][2]}")
exam_id = options[exam_choice][0]

# Confirmation
confirm = input(f"{Fore.RED}[ CONFIRMATION ] - Press Enter to add {intra_id} to the above exam.")

# Build payload
payload = {
	"exams_user": {
		"user_id": student_id
    }
}

response = oauth.post(f"{SITE}/v2/exams/{exam_id}/exams_users", json=payload)

if (response.status_code == 201):
	color = Fore.GREEN
else:
	color = Fore.RED

print(f"{color}{response.status_code} {response.text}")