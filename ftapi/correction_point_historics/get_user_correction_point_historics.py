# get_user_correction_point_historics.py
"""Module for getting correction point historics for a user by login
using the 42 API (v2)."""

from json import dumps as json_dumps
from FtApi import FtApi
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success


def get_correction_point_historics_by_login(ft_api: FtApi | None = None,
                                            login: str | None = None) -> list:
    """Gets correction point historics for a user by login.

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
    ft_write_info(f"GET: {get_url}")
    get_res = ft_api.get(get_url)
    ft_write_success(f"{login}: Correction point historics retrieved.")
    return get_res


def test_get_correction_point_historics_by_login():
    """Test function for getting correction point historics for login."""
    print(json_dumps(get_correction_point_historics_by_login(login="dtrin"),
                     indent=2))
    return


if __name__ == "__main__":
    test_get_correction_point_historics_by_login()
