# mark_test_account.py
"""Pulls the API data for user yeatay
"""

import colorama
from colorama import Fore
from time import sleep
import sys
sys.path.append('ftapi')
from FtApi import FtApi


def main():
    """Pulls the API data for user
    """
    colorama.init(autoreset=True)
    LOGINS = ["dtrin",
              "emars", "elmars", "elamars", "elarmars", "elaramar",
              "emars2", "elmars2", "elamars2", "elarmar2", "elarama2"]

    try:
        ft_api = FtApi()
        SITE = ft_api.site
        for login in LOGINS:
            get_url = f"{SITE}/v2/users?filter[login]={login}"
            user_data = ft_api.get(get_url)
            user_id = user_data[0]['id']
            post_url = f"{SITE}/v2/groups_users"
            payload = dict(
                groups_user=dict(
                    group_id="119",
                    user_id=user_id
                )
            )
            response = ft_api.oauth.post(post_url, json=payload)
            colour = Fore.GREEN
            if int(response.status_code) != 201:
                colour = Fore.RED
            print(f"{colour}{login} ({user_id}): {response.text}")
            sleep(0.5)

    except BaseException as error:
        print(f"Error: {error}")
        exit()

    return


if __name__ == "__main__":
    main()
