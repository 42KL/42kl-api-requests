import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import os
import time
load_dotenv()

UID = os.getenv("42-UID")  # EDIT .env file
SECRET = os.getenv("42-SECRET")  # EDIT .env file
CAMPUS_ID = os.getenv("42-CAMPUS")

if None in [UID, SECRET, CAMPUS_ID]:
	raise (Exception("Env variables are not defined!"))

SITE = "https://api.intra.42.fr"
SCOPE = "public projects"

# Create a client using the OAuth2Session with a BackendApplicationClient
client = BackendApplicationClient(client_id=UID)
oauth = OAuth2Session(client=client)

# Fetch the token using client_credentials flow
token = oauth.fetch_token(
    token_url=f"{SITE}/oauth/token", client_id=UID, client_secret=SECRET, scope=SCOPE
)

# Get all users with pool year 2023 and campus in KL, and check if their piscine user is active
info = []
page_num = 1
while 1:
    response = oauth.get(f"{SITE}/v2/users?filter[primary_campus_id]={CAMPUS_ID}&filter[pool_year]=2023&filter[pool_month]=september&page[size]=100&page[number]={page_num}")
    page_num += 1
    for user in response.json():
        # print(user['login'])
        time.sleep(0.5)
        user_dat = oauth.get(f"{SITE}/v2/users/{user['login']}").json()
        # print(user_dat.json())
        for cursus in user_dat['cursus_users']:
            if cursus['cursus_id'] == 9 and cursus['user']['active?']:
                print(user['login'])                
    if (len(response.json()) < 100):
        break
    time.sleep(0.5)
# Print response status and content
# print(response.status_code)
# print(response.text)
