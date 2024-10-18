import colorama
from colorama import Fore
from dotenv import load_dotenv
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from datetime import datetime as dt, timedelta
import json

colorama.init(autoreset=True)

load_dotenv()

UID = os.getenv("42-UID")  # EDIT .env file
SECRET = os.getenv("42-SECRET")  # EDIT .env file
CAMPUS_ID = os.getenv("42-CAMPUS")

if None in [UID, SECRET, CAMPUS_ID]:
	raise (Exception("Env variables are not defined!"))

# Create a client using the OAuth2Session with a BackendApplicationClient
client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

# Fetch the token using client_credentials flow
SITE = "https://api.intra.42.fr"
SCOPE = "public projects"
token = oauth.fetch_token(
    token_url=f"{SITE}/oauth/token",
    client_id=UID,
    client_secret=SECRET,
    scope=SCOPE
)

# Setting up filters
# # Piscine Pool
POOL_YEAR = input("Enter Piscine pool year: ")
if POOL_YEAR == "":
	print(f"{Fore.RED}Didn't receive any input, quitting.")
	exit()
POOL_MONTH = input("Enter Piscine pool month: ")
if POOL_MONTH == "":
	print(f"{Fore.RED}Didn't receive any input, quitting.")
	exit()

# # Exam
# # Using /v2/campus/:campus_id/exams list exams, limit to the 5 most recent
# # exams either on-going or in the future
get_exam_req = oauth.get(f"{SITE}/v2/campus/{CAMPUS_ID}/exams")
if (get_exam_req.status_code != 200):
	print(f"{FOre.RED}Error on GET request for /v2/campus/:campus_id/exams")
	exit()

exam_data = json.loads(get_exam_req.text)
current_dt = dt.now()
count = 0
options = []

print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'ID': ^9}|{'NAME': ^35}|{'DATE': ^12}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+")

for item in exam_data:
	if count == 5 or current_dt > (dt.fromisoformat((item['end_at'])[:-1]) + timedelta(hours=8)):
		break
	exam_start = item['begin_at'].split('T')[0]
	print(f"{Fore.CYAN}|{count: ^7}|{item['id']: ^9}|{item['name']: ^35}|{exam_start: ^12}|")
	options.append([item['id'], item['name'], exam_start])
	count += 1

print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+\n")

exam_choice = input(f"{Fore.YELLOW}Enter the INDEX of the exam: ")
if exam_choice == "":
	print(f"{Fore.RED}Didn't receive any input, quitting.")
	exit()
exam_choice = int(exam_choice)
print(f"{Fore.CYAN}Selected {options[exam_choice][1]} that starts on {options[exam_choice][2]}")
exam_id = options[exam_choice][0]

# Pulling the data
# # Pulling the project users
proj_slugs = [ proj['slug'] for proj in exam_data[exam_choice]['projects'] ] 
proj_users = []
for proj_id in proj_slugs:
	GET_URL = f"{SITE}/v2/projects/{proj_id}/projects_users"
	GET_URL = f"{GET_URL}?filter[campus]={CAMPUS_ID}"
	GET_URL = f"{GET_URL}&page[size]=100"
	page_num = 1
	while 1:
		response = oauth.get(f"{GET_URL}&page[number]={page_num}")
		if response.status_code != 200:
			print(f"{Fore.RED}{response.status_code}: {response.reason}")
			break
		for item in response.json():
			user = item['user']
			if user['pool_year'] == POOL_YEAR and user['pool_month'] == POOL_MONTH:
				proj_users.append(user['login'])
		page_num += 1
		if (len(response.json()) < 100):
			break
		time.sleep(0.5)

# # Pulling the exam users
GET_URL = f"{SITE}/v2/exams/{exam_id}/exams_users"
response = oauth.get(GET_URL)
if response.status_code != 200:
	print(f"{Fore.RED}{response.status_code}: {response.reason}")
	exit()
exam_users = []
for item in response.json():
	exam_users.append(item['user']['login'])

# Writing data out
# # The SVG image
with open("generate-visuals/exam-sub-status.svg") as infile:
	svg_data = infile.read();
	infile.close()

outfile = str(options[exam_choice][1]).lower().replace(" ", "-")
outfile = f"{outfile}-{options[exam_choice][2]}"
outfile = f"{POOL_YEAR}-{POOL_MONTH}-{outfile}"

with open(f"{outfile}.svg", "w") as out_svg:
	svg_data = svg_data.replace("PU", str(len(proj_users)))
	svg_data = svg_data.replace("EU", str(len(exam_users)))
	print(svg_data, file=out_svg)
	out_svg.close()

# # The data table
json_data = {}
with open(f"{outfile}.json", "w") as out_json:
	bad_users = []
	for user in proj_users:
		if user not in exam_users:
			bad_users.append(user)
	json_data['bad_users'] = bad_users
	json_data['bad_users'].sort()
	json_data['project_users'] = proj_users
	json_data['project_users'].sort()
	json_data['exam_users'] = exam_users
	json_data['exam_users'].sort()
	json.dump(json_data, out_json, indent=4)
	out_json.close()
