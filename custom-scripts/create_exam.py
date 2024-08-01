from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from datetime import datetime as dt, timedelta
import os
import colorama
from colorama import Fore

colorama.init(autoreset=True)

load_dotenv()

# HOW 2 USE:
# JUST RUN python3 create_exam.py
# ALL INPUTS ARE PROMPTED

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


# What do I need :
# exam[name]				// the name of the exam, i.e. CADET: RANKING EXAMS
# exam[begin_at]			// the starting time of the exam, in the format 2015-07-17T15:00:00.000Z
# exam[end_at]				// the ending time of the exam, must be after the begin_at time.
# exam[location]			// the clusters, i.e. "Unit 181"
# exam[ip_range]			// the i.p. range of the machines, i.e. "10.11.0.0/16,10.12.0.0/16, 10.13.0.0/16, 10.14.0.0/16, 10.15.0.0/16"
# exam[campus_id]			// the unique campus id. 42KL is 34
# exam[activate_waitlist] 	// whether to activate waitlist or not, i.e. "false"
# exam[project_ids] 		// the ids of the projects that will be taken for the exam. Must be an array.

#	ids		|	projects
#	1320	|	Exam Rank 02
#	1321	|	Exam Rank 03
#	1322	|	Exam Rank 04
#	1323	|	Exam Rank 05
#	1324	|	Exam Rank 06
#	1301	|	C Piscine Exam 00
#	1302	|	C Piscine Exam 01
#	1303	|	C Piscine Exam 02
#	1304	|	C Piscine Final Exam

# Get which exam session we creating
menu = """
0: C Piscine Exam 00
1: C Piscine Exam 01
2: C Piscine Exam 02
3: C Piscine Final Exam
4: Cadet Ranking Exams
"""
print(f"{Fore.CYAN}Please choose which exam you would like to create, based on the list below;\n{menu}")

choices = [
	[[1301], "C Piscine Exam 00"],
	[[1302], "C Piscine Exam 01"],
	[[1303], "C Piscine Exam 02"],
	[[1304], "C Piscine Final Exam"],
	[[1320, 1321, 1322, 1323, 1324], "Cadet Ranking Exam"],
	[[1320, 1321, 1322, 1323, 1324], "API Test: DO NOT SUBSCRIBE"]
]

exam_choice = int(input(f"{Fore.YELLOW}Type in your choice from 0-4: "))
print(f"{Fore.CYAN}You have chosen {choices[exam_choice][1]}")

# Check for DO NOT SUBSCRIBE anomalies.
ans = input(f"{Fore.YELLOW}Is this a DO NOT SUBSCRIBE session? (Y if yes, otherwise no): ")
if ans == "Y":
	choices[exam_choice][1] = "DO NOT SUBSCRIBE"

# Ask if the exam is to be invisible
invis = input("Is the exam meant to be invisible? (Y if yes, otherwise no): ")
if invis == "Y":
	choices[exam_choice][1] += " (INVISIBLE)"
	vis_state = "false"
else:
	vis_state = "true"

# Ask if the exam is meant to be a pop-up exam, only for Cadet Ranking Exams.
if exam_choice == 4:
	popup = input("Is the exam meant to be a Pop-up? (Y if yes, otherwise no): ")
	if popup == "Y":
		choices[exam_choice][1] = "Pop-Up " + choices[exam_choice][1]

# Get the location of the exam.
# Default for Cadet Ranking Exams - Unit 181
# Default for Piscine - Unit 181, 182
print(f"{Fore.CYAN}\n[ EXAM LOCATION SELECTION ]\n")
choice_arr = [
	["Unit 180", "10.11.0.0/16"],
	["Unit 181", "10.12.0.0/16"],
	["Unit 182", "10.13.0.0/16"],
	["Unit 190", "10.14.0.0/16"],
	["Unit 191", "10.15.0.0/16"],
]
print(f"{Fore.CYAN}Your options are:\n[0] - Unit 180\n[1] - Unit 181\n[2] - Unit 182\n[3] - Unit 190\n[4] - Unit 191")
print(f"{Fore.CYAN}\nPlease type in the index of the intended Units seperated by just commas.\nFor example, '1' stands for just Unit 181, '0,2' stands for Units 180 and 182.")
while (True):
	ip_range = []
	exam_location = []
	raw_input = input(f"{Fore.YELLOW}Type in the index of the Exam Unit(s) (Leave empty for default): ")
	if (raw_input == ""):
		if exam_choice == 4:
			exam_location = "Unit 181"
			ip_range = "10.12.0.0/16"
		elif exam_choice in [0, 1, 2, 3]:
			exam_location = "Unit 181, Unit 182"
			ip_range = "10.12.0.0/16,10.13.0.0/16"
		break
	try:
		input_vals = [int(i) for i in raw_input.split(',')]
		for item in input_vals:
			exam_location.append(choice_arr[item][0])
			ip_range.append(choice_arr[item][1])
		if len(exam_location) == 0:
			raise(Exception("You did not enter a valid exam location."))
		if len(exam_location) == 1:
			sep = ""
		else:
			sep = ", "
		exam_location = sep.join(exam_location)
		ip_range = sep.join(ip_range)
		break
	except Exception as err:
		print(f"{Fore.RED}[ ERROR ] - {err}\nTry again")
		continue

# Get the starting time and duration of the exam. Get the time in Malaysian time, and adjust to Paris time
# Paris time = Malaysia time - 8 hours

# Auto fit duration and time based on choice, but ask just in case.
if exam_choice == 3:
	default_duration = 8
	default_time = "10:30"
elif exam_choice in [4, 5]:
	default_duration = 3
	default_time = "14:00"
else:
	default_duration = 4
	default_time = "14:30"

raw_date = input(f"{Fore.YELLOW}Type in the start date of the exam in the format DD/MM/YYYY, e.g 18/3/2024: ")

# Start time must be in the format of HH:MM, e.g. 9:00 or 15:30
raw_time = input(f"{Fore.YELLOW}Type in the start time of the exam (default is {default_time}): ")
if (raw_time == ""):
	raw_time = default_time

duration = input(f"{Fore.YELLOW}Type in the number of hours the exam will take (default is {default_duration} hours): ")
if (duration == ""):
	duration = default_duration
else:
	duration = int(duration)

raw_start = f"{raw_date} {raw_time}"
parsed_start = dt.strptime(raw_start, "%d/%m/%Y %H:%M")
parsed_start = parsed_start - timedelta(hours=8)
parsed_end = parsed_start + timedelta(hours=duration)

final_start = parsed_start.strftime("%Y-%m-%dT%H:%M:00.000Z")
final_end = parsed_end.strftime("%Y-%m-%dT%H:%M:00.000Z")


# Confirm payload before sending
print(f"{Fore.CYAN}\nSimulated payload - Check for final details")
print(f"{Fore.CYAN}name : {choices[exam_choice][1]}")
print(f"{Fore.CYAN}begin_at : {final_start}")
print(f"{Fore.CYAN}end_at : {final_end}")
print(f"{Fore.CYAN}location : {exam_location}")
print(f"{Fore.CYAN}ip_range : {ip_range}")
print(f"{Fore.CYAN}campus_id : 34")
print(f"{Fore.CYAN}visible: {vis_state}")
print(f"{Fore.CYAN}project_ids : {choices[exam_choice][0]}")

print(f"\n{Fore.RED}CONFIRMATION")
confirmed = input(f"{Fore.YELLOW}Press Enter/Return to confirm the payload.")
print(f"{Fore.CYAN}Payload confirmed, generating and sending API call")

# Build payload
payload = {
	"exam": {
		"name": choices[exam_choice][1],
		"begin_at": final_start,
		"end_at": final_end,
		"location": exam_location,
		"ip_range": ip_range,
		"campus_id": "34",
		"ativate_waitlist": "false",
		"visible": vis_state,
		"project_ids": choices[exam_choice][0]
	}
}

# Make request
response = oauth.post(f"{SITE}/v2/exams", json=payload)

# Print response status and content
if (response.status_code == 201):
	color = Fore.GREEN
else:
	color = Fore.RED
print(f"{color} {response.text}")

