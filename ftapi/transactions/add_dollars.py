# add_dollars.py
"""Adds Alterian dollars to users."""

import sys
from time import sleep
from FtApi import FtApi
from users.get_user_id_by_login import get_user_id_by_login
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_read_file import ft_read_list
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success


def add_dollars(ft_api: FtApi = None,
                login: str = None,
                amount: int = 1,
                reason: str = "") -> None:
    """Adds Alterian dollars to a user.

    Attributes:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.
        login (str): 42 intra login of a user to add dollars to
        amount (int): Number of dollars to add (default is 1).
        reason (str): Reason for adding dollars
    """
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "42 intra login must be given as a non-empty string. Nothing is done."
    assert isinstance(amount, int) and amount > 0, \
        "Dollars amount must be a positive integer. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    user_id = get_user_id_by_login(ft_api=ft_api, login=login)
    payload = {
        "transaction": {
            "value": amount,
            "user_id": user_id,
            "transactable_type": "Airdrop",
            "reason": reason
        }
    }
    post_url = f"{ft_api.site}/v2/transactions"
    post_res = ft_api.oauth.post(post_url, json=payload)
    if int(post_res.status_code) != 201:
        error = f"ERROR: Attempt to add dollars failed for {login}."
        error += f"\n{post_res.status_code}: {post_res.text}."
        raise Exception(error)
    post_res.raise_for_status()
    post_res.close()
    ft_write_success(f"{login}: {amount} dollars added.")


def main():
    """Adds dollars to user(s).
    Gets logins from a newline-separated text file supplied by the command line
    argument, or a single login via interactive prompt if no arguments given.
    Gets one amount and reason interactively that is applied to all logins."""
    USAGE = f"USAGE: python3 {sys.argv[0]} <logins.txt>"
    USAGE += "\n"
    USAGE += "    logins.txt: (Optional) Text file containing intra logins,"
    USAGE += "\n"
    USAGE += "                one per line."
    USAGE += "\n"
    USAGE += "                If not provided, user will be prompted to enter"
    USAGE += "\n"
    USAGE += "                a single login interactively."
    try:
        # Don't do anything if more than 1 parameter is given,
        # if one parameter given, assume it's the one-per-line list of logins
        # to airdrop dollars for.
        # if no parameters given, assume user will supply login via terminal
        # input.
        if len(sys.argv) > 2:
            err_msg = f"ERROR: Too many arguments\n{USAGE}"
            raise Exception(err_msg)
        elif len(sys.argv) == 2:
            LOGINS_FILE = sys.argv[1]
            logins = ft_read_list(LOGINS_FILE)
        else:
            ft_write_info(USAGE)
            login_input = input("Enter a single intra login: ").strip()
            logins = [login_input] if len(login_input) > 0 else []
        # If list of logins is empty, then there is nothing to do!
        assert len(logins) > 0, "No intra logins provided. Nothing to do!"
        # Get amount to airdrop
        amount = None
        while amount is None or int(amount) < 1:
            instruction = "Enter dollars to airdrop"
            instruction += " (must be a positive number): "
            amount = int(input(instruction).strip())
        # Get reason for airdrop
        instruction = "Enter reason for airdrop:"
        reason = input(instruction).strip()
        # Add dollars to each login
        ft_api = FtApi()
        for login in logins:
            add_dollars(ft_api=ft_api,
                        login=login,
                        amount=amount,
                        reason=reason)
            sleep(0.5)
    except BaseException as error:
        ft_handle_error(error)
        return


if __name__ == "__main__":
    main()
