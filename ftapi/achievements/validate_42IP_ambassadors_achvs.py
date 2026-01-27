# validate_42IP_ambassadors_achvs.py
"""Checks status for achievement users, fix by PATCH if required."""

from time import sleep
from FtApi import FtApi
from achievements.FtAchievementUser import FtAchievementUser
from achievements.get_achv_users_by_id import get_achv_users_by_id
from utils.io.ft_write_stderr import ft_write_info, ft_write_success


ACHV_REQS = {1596: 1, 1598: 3, 1599: 5, 1600: 10}


def validate_achv(ft_api: FtApi = None) -> None:
    """Validates if each user's nbr_of_success meets the requirements for
    rewarding each of the achievements, and updates the record via PATCH
    if required.

    Args:
        ft_api (FtApi): An FtApi instance (42 API authentication object).
                        Optional, instantiated if note provided.
    """
    try:
        if ft_api is None or not isinstance(ft_api, FtApi):
            ft_api = FtApi()
        for achv_id in ACHV_REQS.keys():
            achv_users = get_achv_users_by_id(ft_api=ft_api, achv_id=achv_id)
            sleep(0.7)
            for achv_user in achv_users:
                achv_user_id = achv_user["id"]
                user_id = achv_user["user_id"]
                nbr_of_success = achv_user["nbr_of_success"]
                rewarded = nbr_of_success >= ACHV_REQS[achv_id]
                achv_user = FtAchievementUser(user_id=user_id,
                                              achievement_id=achv_id,
                                              nbr_of_success=nbr_of_success,
                                              rewarded=rewarded)
                payload = {"achievements_user": achv_user.asdict()}
                patch_url = f"{ft_api.site}/v2/achievements_users/"
                patch_url += f"{achv_user_id}"
                ft_write_info(f"PATCH {patch_url} {payload}")
                patch_res = ft_api.oauth.patch(patch_url, json=payload)
                patch_res.raise_for_status()
                ft_write_success(f"Validated {achv_id} for {user_id}.")
                patch_res.close()
                sleep(0.7)
        return None
    except Exception as error:
        ft_write_info(f"Error: {error}")
        return None


if __name__ == "__main__":
    validate_achv()
