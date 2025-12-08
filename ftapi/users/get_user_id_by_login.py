# get_user_id_by_login.py
"""Return user_id for given login"""


from FtApi import FtApi


def get_user_by_login(ft_api: FtApi = None, login: str = None) -> list:
    """GET using 42 API the user data for a given login"""
    assert login is not None, "login is undefined, doing nothing."
    assert isinstance(login, str), "Invalid login."
    assert len(login) > 0, "login is empty string, doing nothing."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    get_url = f"{ft_api.site}/v2/users?filter[login]={login}"
    return ft_api.get(get_url)


def get_user_id_by_login(ft_api: FtApi = None, login: str = None) -> str:
    assert login is not None, "login is undefined, doing nothing."
    assert isinstance(login, str), "Invalid login."
    assert len(login) > 0, "login is empty string, doing nothing."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    user_data = get_user_by_login(ft_api=ft_api, login=login)
    if isinstance(user_data, dict) and int(user_data.status_code) != 200:
        raise AssertionError(f"{user_data.status_code}: {user_data.reason}.")
    if len(user_data) == 0:
        raise AssertionError("login not found")
    if len(user_data) > 1:
        raise AssertionError("login not unique")
    assert "id" in user_data[0].keys(), user_data.reason
    return str(user_data[0]['id'])
