from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta
import os
import colorama
import time
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

# First create dt variables that represent the next Wednesday and next Saturday for the week.
# This script has to be run on either Sunday, Monday or Tuesday.
dt_today = dt.now()
num_to_wed = 3 - int(dt_today.strftime("%w"))

dt_wed = dt_today + timedelta(days=num_to_wed)
dt_sat = dt_wed + timedelta(days=3)

wed_start = dt_wed.strftime("%Y-%m-%dT06:00:00.000Z")
wed_end = dt_wed.strftime("%Y-%m-%dT09:00:00.000Z")
sat_start = dt_sat.strftime("%Y-%m-%dT06:00:00.000Z")
sat_end = dt_sat.strftime("%Y-%m-%dT09:00:00.000Z")

# Get exam location
exam_location = input("Type in the exam location (Default is Unit 181GF): ")
if (exam_location == ""):
	exam_location = "Unit 181GF"

payloads = [
	{
		"exam": {
			"name": "Cadet Ranking Exam",
			"begin_at": wed_start,
			"end_at": wed_end,
			"location": exam_location,
			"ip_range": "10.11.0.0/16,10.12.0.0/16, 10.13.0.0/16, 10.14.0.0/16, 10.15.0.0/16",
			"campus_id": "34",
			"activate_waitlist": "false",
			"project_ids": [1320, 1321, 1322, 1323, 1324]
		}
	},
	{
		"exam": {
			"name": "Cadet Ranking Exam",
			"begin_at": sat_start,
			"end_at": sat_end,
			"location": exam_location,
			"ip_range": "10.11.0.0/16,10.12.0.0/16, 10.13.0.0/16, 10.14.0.0/16, 10.15.0.0/16",
			"campus_id": "34",
			"activate_waitlist": "false",
			"project_ids": [1320, 1321, 1322, 1323, 1324]
		}
	}
]

for payload in payloads:
	response = oauth.post(f"{SITE}/v2/exams", json=payload)

	if (response.status_code == 201):
		color = Fore.GREEN
	else:
		color = Fore.RED
	print(f"{color} {response.text}")

	time.sleep(0.5)