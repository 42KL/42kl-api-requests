# create_users.py
"""Creates external users on the intranet for Discovery Piscine
"""

import colorama
from colorama import Fore
import json
import sys
sys.path.append("ftapi")
from FtApi import FtApi


class FtUser:
    """The FtUser class/object contains
    - dictionary to contain data for a user to create on 42 intranet.
    - method to validate if dictionary is valid (no missing required value.
    """

    def __init__(cls, email=None, first_name=None, last_name=None,
                 usual_first_name=None, campus_id=None,
                 cursus_id=None, begin_at=None, end_at=None):
        """on initialisation, dictionary is created.
        """
        cls.required = ["email", "first_name", "last_name", "kind",
                        "campus_id"]
        cls.user = dict(
                user=dict(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        kind="external",
                        skip_welcome_mail="true",
                        campus_id=campus_id
                        )
                )
        if usual_first_name is not None and usual_first_name != "":
            cls.user["user"]["usual_first_name"] = usual_first_name
        cls.cursus = dict(
                cursus_user=dict(
                        cursus_id=cursus_id,
                        begin_at=begin_at
                )
        )
        if end_at is not None and end_at != "":
            cls.cursus["cursus_user"]["end_at"] = end_at

    def __str__(cls):
        """returns the values in the dictionary
        """
        return str(cls.user)

    def __repr__(cls):
        """returns the values in the dictionary
        """
        return repr(cls.user)

    def is_postable(cls):
        """returns if all required parameters are not None
        """
        state = cls.user["user"]
        for key in cls.required:
            if state[key] is None:
                return False
        return True

    def whats_wrong(cls):
        """prints information on what"s wrong (which required value not set)
        """
        is_missing = "is required but not set"
        state = cls.user["user"]
        for key in cls.required:
            if state[key] is None:
                print(f"{Fore.RED}    {key} {is_missing}.")
        return


def main():
    """Creates external users on the intranet for Discovery Piscine
    """
    colorama.init(autoreset=True)
    BEGIN_AT = "2025-02-20T11:10:42.000Z"
    CURSUS_ID = "80"  # This is DISCOVERY PYTHON

    try:
        ft_api = FtApi()
        SITE = ft_api.site
        CAMPUS_ID = ft_api.campus
        ft_user = FtUser(email="elara.mars@outlook.com",
                         first_name="Elara",
                         last_name="Mars",
                         usual_first_name="E",
                         campus_id=CAMPUS_ID,
                         cursus_id=CURSUS_ID,
                         begin_at=BEGIN_AT)
        if ft_user.is_postable() is not True:
            ft_user.whats_wrong()
            raise Exception("Missing values in Payload")
        print(ft_user.user)
        print(f"{Fore.BLUE}POST /v2/users:")
        response = ft_api.oauth.post(f"{SITE}/v2/users",
                                     json=ft_user.user)
        if int(response.status_code) != 201:
            raise Exception(response.text)
        print(response.text)
        ft_user.data = json.loads(response.text)
        ft_user.cursus["cursus_user"]["user_id"] = ft_user.data["id"]
        print(f"{Fore.BLUE}POST /v2/cursus_users:")
        response = ft_api.oauth.post(f"{SITE}/v2/cursus_users",
                                     json=ft_user.cursus)
        if int(response.status_code) != 201:
            raise Exception(response.text)
        print(response.text)
    except BaseException as error:
        print(f"{Fore.RED}Error: {error}")
        exit()

    return


if __name__ == "__main__":
    main()
