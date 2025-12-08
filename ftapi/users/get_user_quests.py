# get_user_quests.py
"""Return quests for given user"""

from time import sleep
from FtApi import FtApi
from FtUtils import ft_write_info
from get_user_id_by_login import get_user_by_login


def get_user_quests_by_id(ft_api: FtApi = None, user_id: str = None) -> list:
    """GET using 42 API the user quests data for a given user_id"""
    assert user_id is not None, "user_id is undefined, doing nothing."
    assert isinstance(user_id, str), "Invalid user_id: not a string."
    assert len(user_id) > 0, "Invalid user_id: cannot be empty."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    get_url = f"{ft_api.site}/v2/users/{user_id}/quests"
    return ft_api.get(get_url)


def get_user_quests_by_login(ft_api: FtApi = None, login: str = None) -> list:
    """GET using 42 API the user quests data for a given login"""
    assert login is not None, "login is undefined, doing nothing."
    assert isinstance(login, str), "Invalid login: not a string."
    assert len(login) > 0, "Invalid login: cannot be empty."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    user_id=get_user_by_login(ft_api, login)
    assert len(user_id) == 1, "Error: Unable to identify unique ID for {login}."
    user_id=f"{user_id[0]['id']}"
    sleep(0.8)
    return get_user_quests_by_id(ft_api=None, user_id=user_id)
