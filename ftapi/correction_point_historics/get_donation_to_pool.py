# get_donation_to_pool.py
"""Module for getting donation to pool for a user by login
using the 42 API (v2)."""

from json import dumps as json_dumps
from FtApi import FtApi
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success
from utils.io.ft_read_file import ft_read_list


def get_donation_to_pool(ft_api: FtApi | None = None,
                         login: str | None = None) -> list:
    """Gets donation to pool for a user by login.

    Attributes:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.
        login (str): 42 intra login of a user to get data for.

    Returns:
        list: list of user correction point historics.
    """
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "42 intra login must be given as a non-empty string. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    get_url = f"{ft_api.site}/v2/users/{login}/correction_point_historics"
    get_url += "?filter[reason]=Provided points to the pool."
    ft_write_info(f"GET: {get_url}")
    get_res = ft_api.get(get_url)
    ft_write_success(f"{login}: Donation to pool retrieved.")
    return get_res


def test_get_donation_to_pool():
    """Test function for getting donation to pool for login."""
    print(json_dumps(get_donation_to_pool(login="dtrin"),
                     indent=2))
    return


def print_donation_to_pool() -> None:
    """Print total donation to pool for list of user."""
    logins = ft_read_list("cadets.lst")
    for login in logins:
        donations = get_donation_to_pool(login=login)
        if len(donations) > 0:
            print(json_dumps({login: donations}, indent=2))
    return None


if __name__ == "__main__":
    print_donation_to_pool()
