# get_achv_rec.py
"""Get achievement user records for a given achievement ID and user_id."""

import json
from FtApi import FtApi
from utils.io.ft_write_stderr import ft_write_error


def get_achv_rec(ft_api: FtApi = None,
                 achv_id: int = None,
                 user_id: str = None) -> list:
    """Gets achievement user records for a given achievement ID and user_id.

    Args:
        ft_api (FtApi): An FtApi instance (42 API authentication object).
                        Optional, instantiated if note provided.
        achv_id (int): ID of the achievement to get user records for.
        user_id (str): User ID to get the achievement records for.

    Returns:
        list: A list of achievement user dictionaries.
    """
    assert achv_id is not None and isinstance(achv_id, int), \
        "Achievement ID must be given as a non-empty integer. Nothing is done."
    assert user_id is not None and isinstance(user_id, str) and \
        user_id.isdigit() and len(user_id) > 0, \
        "User ID must be given as a non-empty string. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    get_url = f"{ft_api.site}/v2/achievements/{achv_id}"
    get_url += f"/achievements_users?filter[user_id]={user_id}"
    return ft_api.get(get_url)


def test() -> None:
    """Test get_achv_rec function.
    Gets and dumps achievement user records for achievement ID 1596
    (MissionLegacy 1) for user ID 238343.
    """
    try:
        ft_api = FtApi()
        res = get_achv_rec(ft_api=ft_api, achv_id=1596, user_id="238343")
        print(json.dumps(res, indent=4))
        return None
    except Exception as error:
        ft_write_error(f"Error: {error}")
        return None


if __name__ == "__main__":
    test()
