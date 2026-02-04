# add_achv_to_login.py
"""Adds an achievement to a user login."""

from time import sleep
from FtApi import FtApi
from achievements.FtAchievementUser import FtAchievementUser
from achievements.get_achv_rec import get_achv_rec
from users.get_user_id_by_login import get_user_id_by_login
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success


def add_achv_to_login(ft_api: FtApi = None,
                      achv_id: int = None,
                      login: str = None) -> None:
    """Adds an achievement to a user login.

    Args:
        ft_api (FtApi): An FtApi instance (42 API authentication object).
                        Optional, instantiated if note provided.
        achv_id (int): ID of the achievement to add for user.
        login (str): User login to add the achievement to.
    """
    assert achv_id is not None and isinstance(achv_id, int), \
        "Achievement ID must be given as a non-empty integer. Nothing is done."
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "User login must be given as a non-empty string. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    USER_ID = get_user_id_by_login(ft_api=ft_api, login=login)
    sleep(0.7)
    achv_rec = get_achv_rec(ft_api=ft_api, achv_id=achv_id, user_id=USER_ID)
    sleep(0.7)
    if len(achv_rec) == 0:
        post_url = f"{ft_api.site}/v2/achievements_users"
        achv_user = FtAchievementUser(user_id=USER_ID,
                                      achievement_id=achv_id,
                                      nbr_of_success=1)
        payload = {"achievements_user": achv_user.asdict()}
        ft_write_info(f"POST {post_url} {payload}")
        post_res = ft_api.oauth.post(post_url, json=payload)
        post_res.raise_for_status()
        ft_write_success(f"Achievement {achv_id} unlocked for {login}.")
        post_res.close()
    else:
        achv_user_id = achv_rec[0]["id"]
        nbr_of_success = achv_rec[0]["nbr_of_success"] + 1
        achv_user = FtAchievementUser(user_id=USER_ID,
                                      achievement_id=achv_id,
                                      nbr_of_success=nbr_of_success)
        payload = {"achievements_user": achv_user.asdict()}
        patch_url = f"{ft_api.site}/v2/achievements_users/{achv_user_id}"
        ft_write_info(f"PATCH {patch_url} {payload}")
        patch_res = ft_api.oauth.patch(patch_url, json=payload)
        patch_res.raise_for_status()
        ft_write_success(
            f"Achievement {achv_id} updated for {login} "
            f"with nbr_of_success = {nbr_of_success}.")
        patch_res.close()
    return None


def test() -> None:
    """Test add_achv_to_login function.
    Adds achievement ID 1596 (MissionLegacy 1) to user login "adzmusta".
    """
    try:
        ft_api = FtApi()
        add_achv_to_login(ft_api=ft_api, achv_id=1598, login="dtrin")
        return None
    except Exception as error:
        ft_handle_error(error)  # will exit(1)
        return None


if __name__ == "__main__":
    test()
