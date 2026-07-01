# add_user_to_cursus.py
"""Adds a user on the intranet to a cursus."""


import sys
from FtApi import FtApi
from FtCursus import compute_cursus_end_from_begin
from FtUser import FtCursusUser
from users.get_user_id_by_login import get_user_id_by_login
from utils.ft_datetime import is_valid_date
from utils.io.ft_handle_error import ft_handle_error


def add_user_id_to_cursus(ft_api: FtApi = None,
                          user_id: str = None,
                          cursus_id: str = None,
                          begin_date: str = None) -> dict:
    """Create a cursus user using 42 API (v2)"""
    assert user_id is not None and isinstance(user_id, str) and \
        len(user_id) > 0, "Undefined/invalid user_id, doing nothing."
    assert cursus_id is not None and isinstance(cursus_id, str) and \
        len(cursus_id) > 0, "Undefined/invalid cursus_id, doing nothing."
    assert begin_date is not None and isinstance(begin_date, str) and \
        len(begin_date) > 0 and is_valid_date(begin_date), \
        "Undefined/invalid begin_date, doing nothing."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    BEGIN_AT = f"{begin_date} 00:00:42"
    END_AT = compute_cursus_end_from_begin(cursus_id=cursus_id,
                                           begin_date=begin_date)
    cursus_user = FtCursusUser(user_id=user_id, cursus_id=cursus_id,
                               begin_at=BEGIN_AT, end_at=END_AT)
    cursus_user = {"cursus_user": cursus_user.asdict()}
    post_url = f"{ft_api.site}/v2/cursus_users"
    post_re = ft_api.oauth.post(post_url, json=cursus_user)
    post_re.raise_for_status()
    return post_re


def add_login_to_cursus(ft_api: FtApi = None,
                        login: str = None,
                        cursus_id: str = None,
                        begin_date: str = None) -> dict:
    """Create a cursus user using 42 API (v2)"""
    assert login is not None and isinstance(login, str) and \
        len(login) > 0, "Undefined/invalid login, doing nothing."
    assert cursus_id is not None and isinstance(cursus_id, str) and \
        len(cursus_id) > 0, "Undefined/invalid cursus_id, doing nothing."
    assert begin_date is not None and isinstance(begin_date, str) and \
        len(begin_date) > 0 and is_valid_date(begin_date), \
        "Undefined/invalid begin_date, doing nothing."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    user_id = get_user_id_by_login(ft_api=ft_api, login=login)
    return add_user_id_to_cursus(ft_api=ft_api,
                                 user_id=user_id,
                                 cursus_id=cursus_id,
                                 begin_date=begin_date)


def main():
    """CLI for adding user login to cursus."""
    USAGE = f"Usage: python3 {sys.argv[0]} LOGIN CURSUS_ID BEGIN_DATE"
    try:
        if len(sys.argv) != 4:
            raise Exception(USAGE)
        LOGIN = sys.argv[1]
        CURSUS_ID = sys.argv[2]
        BEGIN_DATE = sys.argv[3]
        add_login_to_cursus(ft_api=None,
                            login=LOGIN,
                            cursus_id=CURSUS_ID,
                            begin_date=BEGIN_DATE)
    except BaseException as err:
        ft_handle_error(err)


if __name__ == "__main__":
    main()
