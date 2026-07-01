# get_scale_teams_by_login.py
"""Get all scale teams associated with a given login."""


import json
from FtApi import FtApi
from utils.io.ft_handle_error import ft_handle_error
from users.get_user_id_by_login import get_user_id_by_login


def get_scale_teams_by_login(ft_api: FtApi, login: str) -> list[dict]:
    """Get all scale teams associated with a given login.

    Args:
        ftapi (FtApi): An authenticated FtApi instance.
        login (str): The login of the user.

    Returns:
        list[dict]: A list of scale teams associated with the user."""
    try:
        user_id = get_user_id_by_login(ft_api, login)
        url = f"{ft_api.site}/v2/users/{user_id}/scale_teams"
        return ft_api.get(url)
    except Exception:
        raise


if __name__ == "__main__":
    """Get all scale teams for a given login and print them."""
    try:
        LOGIN = input("Enter login to get scale teams for: ").strip()
        ft_api = FtApi()
        scale_teams = get_scale_teams_by_login(ft_api, LOGIN)
        print(json.dumps(scale_teams, indent=4))
    except Exception as error:
        ft_handle_error(error)  # will exit(1)
