# renove_correction_points.py
"""Removes correction points from users."""

import sys
from time import sleep
from FtApi import FtApi
from utils.io.ft_read_file import ft_read_list
from utils.io.ft_write_stderr import ft_write_error, \
                                     ft_write_info, \
                                     ft_write_success


def remove_correction_points(ft_api: FtApi = None,
                             login: str = None,
                             amount: int = 1,
                             reason: str = "") -> None:
    """Removes correction points from a user.

    Attributes:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.
        login (str): 42 intra login of a user to remove correction points from
        amount (int): Number of correction points to remove (default is 1).
        reason (str): Reason for removing correction points (optional).
    """
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "42 intra login must be given as a non-empty string. Nothing is done."
    assert isinstance(amount, int) and amount > 0, \
        "Correction points amount must be a positive integer. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    delete_url = f"{ft_api.site}/v2/users/{login}/correction_points/remove"
    payload = {"reason": reason, "amount": str(amount)}
    ft_write_info(f"DELETE: {delete_url} {payload}")
    delete_res = ft_api.oauth.delete(delete_url, json=payload)
    if int(delete_res.status_code) != 200:
        error = f"ERROR: Attempt to remove points failed for {login}."
        error += f"\n{delete_res.status_code}: {delete_res.text}."
        raise Exception(error)
    delete_res.raise_for_status()
    ft_write_success(f"{login}: {amount} points removed.")
    delete_res.close()
    return


def main():
    """Removes correction points from user(s).
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
        if len(sys.argv) == 2:
            logins_file = sys.argv[1]
            logins = ft_read_list(logins_file)
        else:
            login_input = input("Enter a single intra login: ").strip()
            logins = [login_input] if len(login_input) > 0 else []
        amount_input = input("Enter number of correction points to remove: ")
        amount = int(amount_input)
        reason = input("Enter reason for removing correction points: ").strip()
        ft_api = FtApi()
        for login in logins:
            remove_correction_points(ft_api, login, amount, reason)
            sleep(0.5)
    except BaseException as error:
        ft_write_error(error)
        return
    return


if __name__ == "__main__":
    main()
