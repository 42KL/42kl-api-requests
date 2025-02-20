# create_users.py
"""Creates external users on the intranet for Discovery Piscine
"""

import colorama
from colorama import Fore
#from datetime import datetime as dt
import json
import sys
sys.path.append('ftapi')
from FtApi import FtApi


class FtUser:
    """The FtUser class/object contains
    - dictionary to contain data for a user to create on 42 intranet.
    - method to validate if dictionary is valid (no missing required value.
    """

    def __init__(cls, email=None, first_name=None, last_name=None,
                 campus_id=None):
        """on initialisation, dictionary is created.
        """
        cls.params = dict(
                user=dict(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        kind="external",
                        campus_id=campus_id
                        )
                )
        cls.required = ["email", "first_name", "last_name", "kind", "campus_id"]

    def __str__(cls):
        """returns the values in the dictionary
        """
        return str(cls.params)

    def __repr__(cls):
        """returns the values in the dictionary
        """
        return repr(cls.params)

    def is_postable(cls):
        """returns if all required parameters are not None
        """
        state = cls.params["user"]
        for key in cls.required:
            if isinstance(key, dict):
                for subkey in key.keys():
                    realkeys = key[subkey]
                    for realkey in realkeys:
                        if state[subkey][realkey] is None:
                            return False
            else:
                if state[key] is None:
                    return False
        return True

    def whats_wrong(cls):
        """prints information on what's wrong (which required value not set)
        """
        print(f"{Fore.RED}Error: Invalid params")
        is_missing = "is required but not set"
        state = cls.params["user"]
        for key in cls.required:
            if isinstance(key, dict):
                for subkey in key.keys():
                    realkeys = key[subkey]
                    for realkey in realkeys:
                        if state[subkey][realkey] is None:
                            print(f"{Fore.RED}    {realkey} {is_missing}.")
            else:
                if state[key] is None:
                    print(f"{Fore.RED}    {key} {is_missing}.")
        return


def main():
    """Creates external users on the intranet for Discovery Piscine
    """
    colorama.init(autoreset=True)
#    POOL_YEAR="2025"
#    POOL_MONTH="mar"
#    BEGIN_AT="2025-02-20T07:00:00.000Z"
#    CURSUS_ID="80" # This is DISCOVERY PYTHON
#    LANGUAGE_ID="2" # This is ENGLISH

    try:
        ft_api = FtApi()
        SITE = ft_api.site
        CAMPUS_ID = ft_api.campus
        ft_user = FtUser(email="elara.mars@outlook.com",
                         first_name="Elara",
                         last_name="Mars",
                         campus_id=CAMPUS_ID)
        if ft_user.is_postable() is True:
            print(ft_user.params)
            response = ft_api.oauth.post(f"{SITE}/v2/users",
                                         json=ft_user.params)
            colour = Fore.GREEN
            if int(response.status_code) != 201:
                colour = Fore.RED
            print(f"{colour}{response.text}")
        else:
            ft_user.whats_wrong()
    except BaseException as error:
        print(f"{Fore.RED}Error: {error}")
        exit()

    return


if __name__ == "__main__":
    main()
