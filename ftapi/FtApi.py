# FtApi.py
"""
FtApi: Authenticate on 42API using OAuth 2.0
"""


from dotenv import load_dotenv
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from time import sleep


class FtApi:
    """
    __init__(): define vars, load creds, authenticate
    """
    def __init__(cls):
        cls.site = "https://api.intra.42.fr"
        cls.scope = "public projects"
        cls.campus = None
        cls.oauth = None
        cls.token = None
        uid, secret, cls.campus = cls.load_env()
        cls.authenticate(uid, secret)

    """
    load_env(): loads authentication creds from the environment file
    """
    def load_env(cls):
        load_dotenv()
        uid = os.getenv("42-UID")
        secret = os.getenv("42-SECRET")
        campus = os.getenv("42-CAMPUS")
        if None in [uid, secret, campus]:
            raise Exception("Env variables not defined!")
        return uid, secret, campus

    """
    authenticate(): authenticate on 42API using OAuth 2.0
    """
    def authenticate(cls, uid, secret):
        client = BackendApplicationClient(client_id=uid)
        cls.oauth = OAuth2Session(client=client)
        cls.token = cls.oauth.fetch_token(
            token_url=f"{cls.site}/oauth/token",
            client_id=uid,
            client_secret=secret,
            scope=cls.scope
        )
        if cls.token is None:
            raise Exception("Unknown authentication failure.")

    """
    get(url): fetch API data using OAuth 2.0
    """
    def get(cls, url):
        if url.find("?") >= 0:
            get_url = f"{url}&page[size]=100"
        else:
            get_url = f"{url}?page[size]=100"
        responses = []
        page_num = 1
        while True:
            page_response = cls.oauth.get(f"{get_url}&page[number]={page_num}")
            page_num += 1
            if page_response.status_code != 200:
                error_message = "GET failure, status_code"
                error_message = f"{error_message} {page_response.status_code}"
                raise Exception(error_message)
            for response in page_response.json():
                responses.append(response)
            if len(page_response.json()) < 100:
                break
            sleep(0.5)
        return responses
