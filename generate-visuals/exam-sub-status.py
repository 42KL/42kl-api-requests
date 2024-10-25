import colorama
from colorama import Fore
from FtApi import FtApi
from datetime import datetime as dt, timedelta
import json

colorama.init(autoreset=True)

ft_api = FtApi()
SITE=ft_api.site
CAMPUS_ID = ft_api.campus

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
exam_data = ft_api.get(f"{SITE}/v2/campus/{CAMPUS_ID}/exams")
current_dt = dt.now()
count = 0
options = []

print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+")
print(f"{Fore.CYAN}|{'INDEX': ^7}|{'ID': ^9}|{'NAME': ^35}|{'DATE': ^12}|")
print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+")

for item in exam_data:
#	if count == 5 or current_dt > (dt.fromisoformat((item['end_at'])[:-1]) + timedelta(hours=8)):
#		break
	exam_start = item['begin_at'].split('T')[0]
	item_name = item['name']
	if len(item_name) > 33:
		item_name = f"{item_name[:30]}..."
	print(f"{Fore.CYAN}|{count: ^7}|{item['id']: ^9}|{item_name: ^35}|{exam_start: ^12}|")
	options.append([item['id'], item['name'], exam_start])
	count += 1

print(f"{Fore.CYAN}+{'':-^7}+{'':-^9}|{'':-^35}+{'':-^12}+\n")

if len(options) == 0:
	exit()

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
	proj_user_data = ft_api.get(GET_URL)
	for item in proj_user_data:
		user = item['user']
		if user['pool_year'] == POOL_YEAR and user['pool_month'] == POOL_MONTH:
			proj_users.append(user['login'])

# # Pulling the exam users
GET_URL = f"{SITE}/v2/exams/{exam_id}/exams_users"
response = ft_api.get(GET_URL)
exam_users = []
for item in response:
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
