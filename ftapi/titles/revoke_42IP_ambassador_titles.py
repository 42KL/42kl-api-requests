# revoke_42IP_ambassador_titles.py
"""Revoke 42IP ambassador titles from all users using 42 API (v2)."""

from time import sleep
from FtApi import FtApi
from titles.get_titles_users_by_id import get_titles_users_by_id
from titles.revoke_title import revoke_title


TITLE_IDS = [2653, 2654, 2655]


def revoke_titles(ft_api: FtApi = None) -> None:
    """Revoke all 42IP ambassador titles from all users using 42 API (v2).

    Args:
        ft_api (FtApi): An FtApi instance (42 API authentication object).
                        Optional, instantiated if note provided.
    """
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    for title_id in TITLE_IDS:
        title_users = get_titles_users_by_id(ft_api=ft_api,
                                             title_id=title_id)
        for title_user in title_users:
            title_user_id = title_user.get("id")
            revoke_title(ft_api=ft_api, title_user_id=title_user_id)
            sleep(0.7)
    return None


if __name__ == "__main__":
    revoke_titles()
