# FtApi.py


from dotenv import load_dotenv
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from time import sleep


class FtApi:
    """The FtApi class/object contains methods to
    - read uid and secret from an .env file.
    - authenticate on 42 API.
    - fetch data from 42 API.
    """

    def __init__(cls):
        """on instantialisation, define attributes, load creds from .env file, 
        authenticate on the 42 API.
        """
        cls.site = "https://api.intra.42.fr"
        cls.scope = "public projects"
        cls.campus = None
        cls.oauth = None
        cls.token = None
        uid, secret, cls.campus = cls.load_env()
        cls.authenticate(uid, secret)

    def __str__(cls):
        """returns the authentication status on 42 API.
        """
        stat = ""
        if cls.token is None:
            stat = "Not authenticated"
        else:
            stat = "Authenticated"
        stat = f'{stat} for "{cls.scope}" on "{cls.site}".'
        return stat

    def __repr__(cls):
        """returns values for all attributes
        """
        dets = f"site = {cls.site}"
        dets = f"{dets}\nscope = {cls.scope}"
        dets = f"{dets}\ncampus = {cls.campus}"
        dets = f"{dets}\ntoken = {str(cls.token)}"
        return dets

    def load_env(cls):
        """loads authentication creds from the .env file
        """
        load_dotenv()
        uid = os.getenv("42-UID")
        secret = os.getenv("42-SECRET")
        campus = os.getenv("42-CAMPUS")
        if None in [uid, secret, campus]:
            raise Exception("Env variables not defined!")
        return uid, secret, campus

    def authenticate(cls, uid, secret):
        """authenticate on 42 API using OAuth 2.0
        """
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

    def get(cls, url):
        """fetch data using 42 API call
        """
        if url.find("?") >= 0:
            get_url = f"{url}&page[size]=100"
        else:
            get_url = f"{url}?page[size]=100"
        responses = []
        page_num = 1
        while True:
            page_response = cls.oauth.get(f"{get_url}&page[number]={page_num}")
            if page_response.status_code != 200:
                error_message = "GET failure, status_code"
                error_message = f"{error_message} {page_response.status_code}"
                error_message = f"{error_message}: {page_response.reason}"
                raise Exception(error_message)
            for response in page_response.json():
                responses.append(response)
            if len(page_response.json()) < 100:
                page_response.close()
                break
            page_response.close()
            page_num += 1
            sleep(0.8)
        return responses
