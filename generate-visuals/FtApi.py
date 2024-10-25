# FtApi.py

from dotenv import load_dotenv
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


"""
ApiToken: Authenticate on 42API using OAuth 2.0
"""
class FtApi:
	def __init__(self):
		self.site = "https://api.intra.42.fr"
		self.scope = "public projects"
		self.campus = None
		self.token = None
		self.oauth = None
		uid, secret, self.campus = self.loadEnvs()
		self.authenticate(uid, secret)

	"""
	loadEnvs(): loads authentication credentials from the environment file
	"""
	def loadEnvs(self):
		try:
				load_dotenv()
		except:
			print("Error loading .env file.")
		uid = os.getenv("42-UID")
		secret = os.getenv("42-SECRET")
		campus = os.getenv("42-CAMPUS")
		if None in [uid, secret, campus]:
			raise Exception("Env variables not defined!")
		return uid, secret, campus

	"""
	authenticate(): authenticate on 42API using OAuth 2.0
	"""
	def authenticate(self, uid, secret):
		client = BackendApplicationClient(client_id=uid)
		self.oauth = OAuth2Session(client=client)
		self.token = self.oauth.fetch_token(
			token_url=f"{self.site}/oauth/token",
			client_id=uid,
			client_secret=secret,
			scope=self.scope
		)

	"""
	get(url): fetch API data using OAuth 2.0 
	"""
	def get(self, url):
		if url.find("?") >= 0:
			get_url = f"{url}&page[size]=100"
		else:
			get_url = f"{url}?page[size]=100"
		responses = []
		page_num = 1
		while True:
			page_response = self.oauth.get(f"{get_url}&page[number]={page_num}")
			page_num += 1
			if page_response.status_code != 200:
				raise Exception("Error getting API request response.")
			for response in page_response.json():
				responses.append(response)
			if len(page_response.json()) < 100:
				break
			time.sleep(0.5)
		return responses
