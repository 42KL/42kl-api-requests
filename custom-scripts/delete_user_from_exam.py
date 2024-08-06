from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import json
import colorama
from datetime import datetime as dt, timedelta
from colorama import Fore

colorama.init(autoreset=True)

load_dotenv()

# Yay API token stuff
UID = os.getenv("42-UID")
SECRET = os.getenv("42-SECRET")
CAMPUS_ID = os.getenv("42-CAMPUS")

if None in [UID, SECRET, CAMPUS_ID]:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public"

client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(
	token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Just list exams and list down the registered Cadets. Delete from there.
get_exam_req = oauth.get(f"{SITE}/v2/campus/{CAMPUS_ID}/exams")

if get_exam_req.status_code != 200:
	print(f"{Fore.RED}[ ERROR ] - Returned code {get_exam_req.status_code}\n[ ERROR ] - {get_exam_req.text}")
	raise Exception(f"Error occured while getting exams of campus {CAMPUS_ID}")

exam_data = json.loads(get_exam_req.text)
current_dt = dt.now()

exam_options = []
count = 0

print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}+{'':-^35}+{'':-^14}+{'':-^14}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'EXAM ID': ^9}|{'EXAM': ^35}|{'START DATE': ^14}|{'START TIME': ^14}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}+{'':-^35}+{'':-^14}+{'':-^14}+")

for exam in exam_data:
	if current_dt > (dt.fromisoformat((exam["end_at"])[:-1]) + timedelta(hours=8)):
		# Any exams past this point has already passed.
		break
	exam_start_dt = dt.fromisoformat((exam["begin_at"])[:-1]) + timedelta(hours=8)
	start_date = exam_start_dt.strftime("%d/%m/%Y")
	start_time = exam_start_dt.strftime("%H:%M")
	print(f"{Fore.CYAN}|{count: ^7}|{exam['id']: ^9}|{exam['name']: ^35}|{start_date: ^14}|{start_time: ^14}|")
	exam_options.append([exam['name'], exam['id']])
	count += 1

print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}+{'':-^35}+{'':-^14}+{'':-^14}+")

if count == 0:
	print(f"{Fore.GREEN}There are no exams currently ongoing / pending")
	exit()
elif count == 1:
	exam_choice = 0
else:
	exam_choice = int(input(f"\n{Fore.YELLOW}Type in the index of the exam: "))

exam_id = exam_options[exam_choice][1]
print(f"{Fore.CYAN}Chosen {exam_options[exam_choice][0]} with ID {exam_id}")

# Now that we have found the target exam, list down the users of the exam and prompt which one to
# delete.
exam_users_req = oauth.get(f"{SITE}/v2/exams/{exam_id}/exams_users")

if exam_users_req.status_code != 200:
	print(f"{Fore.RED}[ ERROR ] - Returned code {exam_users_req.status_code}\n[ ERROR ] - {exam_users_req.text}")
	raise Exception("Error occured while getting exam users!")

exam_users = json.loads(exam_users_req.text)

if len(exam_users) == 0:
	print(f"{Fore.GREEN}No Users have registered for this Exam Event.")
	exit()

count = 0
user_options = []

print(f"{Fore.CYAN}\n+{'':-^7}+{'':-^11}+{'':-^13}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'USER ID': ^11}|{'CADET': ^13}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^11}+{'':-^13}+")

for user in exam_users:
	print(f"{Fore.CYAN}|{count: ^7}|{user['id']: ^11}|{user['user']['login']: ^13}|")
	user_options.append([user['user']['login'], user['id']])
	count += 1

print(f"{Fore.CYAN}+{'':-^7}+{'':-^11}+{'':-^13}+")

if count == 0:
	print(f"{Fore.GREEN}No Exam Users found for this exam!")
	exit()

while (True):
	user_choice = input(f"{Fore.YELLOW}\nType in the index or login of the user: ")
	try:
		user_choice = int(user_choice)
	except ValueError:
		print(f"{Fore.CYAN}Non-integer value detected. Attempting login search.")
		login_list = [i[0] for i in user_options]
		if user_choice not in login_list:
			print(f"{Fore.RED}User {user_choice} not found, please try again!")
			continue
		exam_user = user_options[login_list.index(user_choice)]
		break
	else:
		if user_choice < 0 or user_choice >= len(user_options):
			print(f"{Fore.RED}[ ERROR ] - Not a valid index, please try again.")
			continue
		exam_user = user_options[user_choice]
		break

print(f"{Fore.CYAN}You have chosen the exam user {exam_user[0]} with ID {exam_user[1]}")
input(f"{Fore.RED}[ CONFIRMATION ] - Press Enter/Return to delete the above Exam User.")

del_req = oauth.delete(f"{SITE}/v2/exams/{exam_id}/exams_users/{exam_user[1]}")

if del_req.status_code == 204:
	print(f"{Fore.GREEN}Exam User has been successfully deleted.")
	exit()
print(f"{Fore.RED}[ ERROR ] - Returned code {del_req.status_code}\n[ ERROR ] - {del_req.text}")