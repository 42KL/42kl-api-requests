# add_42IP_ambassadors.py
"""Adds an achievement to a list of user logins."""

from time import sleep
import sys
from FtApi import FtApi
from utils.io.ft_write_stderr import ft_write_error
from achievements.add_achv_to_login import add_achv_to_login
from utils.io.ft_read_file import ft_read_list


ACHV_IDS = [1596, 1598, 1599, 1600]


def add_42IP_ambassadors() -> None:
    """Adds the 42IP ambassadors achievements to a list of user logins.

    Checks command line arguments for a file containing user logins,
    one login per line. Otherwise, prompts user to input logins via console.

    Updates all predefined 42IP ambassador achievements for each user."""
    USAGE_MSG = "USAGE: python3 {sys.argv[0]} user_list.txt"

    try:
        ft_api = FtApi()
        if len(sys.argv) > 2:
            raise Exception(f"ERROR: Too many arguments.\n{USAGE_MSG}")
        elif len(sys.argv) == 2:
            login_list = ft_read_list(sys.argv[1])
        elif len(sys.argv) < 2:
            login_list = input("Enter logins separated by commas: ")
            login_list = [x.strip() for x in login_list.split(",")]
        assert len(login_list) > 0, \
            "No user logins provided. Nothing is done."
        for achv_id in ACHV_IDS:
            for login in login_list:
                add_achv_to_login(ft_api=ft_api, achv_id=achv_id, login=login)
                sleep(0.7)
    except BaseException as error:
        ft_write_error(f"ERROR: {error}")
        return None


if __name__ == "__main__":
    add_42IP_ambassadors()
