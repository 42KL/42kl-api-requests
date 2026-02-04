# add_correction_points.py
"""Adds correction points to users."""

import sys
from time import sleep
from FtApi import FtApi
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_read_file import ft_read_list
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success


def add_correction_points(ft_api: FtApi = None,
                          login: str = None,
                          amount: int = 1,
                          reason: str = "") -> None:
    """Adds correction points to a user.

    Attributes:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.
        login (str): 42 intra login of a user to add correction points to
        amount (int): Number of correction points to add (default is 1).
        reason (str): Reason for adding correction points
    """
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "42 intra login must be given as a non-empty string. Nothing is done."
    assert isinstance(amount, int) and amount > 0, \
        "Correction points amount must be a positive integer. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    post_url = f"{ft_api.site}/v2/users/{login}/correction_points/add"
    payload = {"reason": reason, "amount": str(amount)}
    ft_write_info(f"POST: {post_url} {payload}")
    post_res = ft_api.oauth.post(post_url, json=payload)
    if int(post_res.status_code) != 200:
        error = f"ERROR: Attempt to add correction points failed for {login}."
        error += f"\n{post_res.status_code}: {post_res.text}."
        raise Exception(error)
    post_res.raise_for_status()
    ft_write_success(f"{login}: {amount} points added.")
    post_res.close()
    return


def main():
    """Adds correction points to user(s).
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
        if len(sys.argv) > 2:
            err_msg = f"ERROR: Too many arguments\n{USAGE}"
            raise Exception(err_msg)
        elif len(sys.argv) == 2:
            LOGINS_FILE = sys.argv[1]
            logins = ft_read_list(LOGINS_FILE)
        else:
            login_input = input("Enter a single intra login: ").strip()
            logins = [login_input] if len(login_input) > 0 else []
        if len(logins) == 0:
            raise Exception("No intra logins provided. Nothing is done.")
        ft_api = FtApi()
        amount = 1
        amount_input = input("Enter number of points to add: ").strip()
        if amount_input.isdigit() and int(amount_input) > 0:
            amount = int(amount_input)
        else:
            ft_write_info(f"Unrecognised input, defaulting to {amount} point.")
        reason_input = input("Enter reason for adding points: ").strip()
        for login in logins:
            add_correction_points(ft_api=ft_api,
                                  login=login,
                                  amount=amount,
                                  reason=reason_input)
            sleep(0.5)
    except BaseException as error:
        ft_handle_error(error)  # will exit(1)
        return


if __name__ == "__main__":
    main()
