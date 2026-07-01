# mark_test_account.py
"""Pulls the API data for user yeatay
"""

import sys
from time import sleep
from FtApi import FtApi
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success
from utils.io.ft_read_file import ft_read_list
from users.get_user_id_by_login import get_user_id_by_login


def mark_test_account(ft_api: FtApi = None,
                      login: str = None) -> None:
    """Marks the given intra login as a test account
    by adding it to group 119 (Test Accounts Group)

    Attributes:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.
        login (str): 42 intra login of a user to mark as test account
    """
    assert login is not None and isinstance(login, str), \
        "42 Intra login must be given as a string."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    SITE = ft_api.site
    user_id = get_user_id_by_login(ft_api=ft_api, login=login)
    post_url = f"{SITE}/v2/groups_users"
    payload = dict(
        groups_user=dict(
            group_id="119",
            user_id=user_id
        )
    )
    ft_write_info(f"POST: {post_url} {login} ({user_id})")
    response = ft_api.oauth.post(post_url, json=payload)
    if int(response.status_code) != 201:
        error = "ERROR: Attempt to mark user as test account failed."
        error += f"\n{response.status_code}: {response.text}."
        raise Exception(error)
    ft_write_success(f"{login} ({user_id}): {response.text}")
    response.raise_for_status()
    response.close()
    return


def main():
    """Reads a text file containing a list of intra logins (one per line), and
    marks each login as a test account.
    This is done by adding the user to group 119 (Test Accounts Group).
    Programme checks if file path is provided as a command-line argument,
    and interactively prompts the user if not.

    Depends:
        FtApi: 42 API authentication object.
        ft_read_list: Function to read a list of logins from a file.
        ft_write_error: Function to log error messages to stderr.
        ft_write_info: Function to log informational messages to stderr.
        ft_write_success: Function to log success messages to stderr.
        get_user_id_by_login: Function to get user ID from intra login.
    """
    USAGE = f"Usage: python3 {sys.argv[0]} <logins.txt>"

    try:
        if len(sys.argv) > 2:
            err_msg = f"ERROR: Too many arguments\n{USAGE}"
            raise Exception(err_msg)
        elif len(sys.argv) == 2:
            LOGINS_FILE = sys.argv[1]
        else:
            LOGINS_FILE = input("Enter path to file containing intra logins: ")
        LOGINS = ft_read_list(LOGINS_FILE)
        if not LOGINS or len(LOGINS) == 0:
            error = "ERROR: Could not read logins from input file"
            error += f": {LOGINS_FILE}."
            raise Exception(error)
        print(LOGINS)
        ft_api = FtApi()
        for login in LOGINS:
            mark_test_account(ft_api=ft_api, login=login)
            sleep(0.5)
    except BaseException as error:
        ft_handle_error(error)  # will exit(1)
    return


if __name__ == "__main__":
    main()
