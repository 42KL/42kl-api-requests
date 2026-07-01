# get_achv_users_by_id.py
"""Get achievements users for a given achievement ID using 42 API (v2)."""

import json
from FtApi import FtApi
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_write_stderr import ft_write_info


def get_achv_users_by_id(ft_api: FtApi = None,
                         achv_id: int = None) -> list:
    """Get achievements users for a given achievement ID using 42 API (v2).

    Args:
        ft_api (FtApi): An FtApi instance (42 API authentication object).
                        Optional, instantiated if note provided.
        achv_id (int): ID of the achievement to GET users for.

    Returns:
        list: A list of achievement user dictionaries.
    """
    assert achv_id is not None and isinstance(achv_id, int), \
        "Achievement ID must be given as a non-empty integer. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    get_url = f"{ft_api.site}/v2/achievements/{achv_id}"
    get_url += "/achievements_users"
    ft_write_info(f"GET {get_url}")
    return ft_api.get(get_url)


def test() -> None:
    """Test get_achv_users_by_id function.
    Gets and dumps achievement users for achievement ID 1596,
    which is MissionLegacy 1.
    """
    try:
        ft_api = FtApi()
        res = get_achv_users_by_id(ft_api=ft_api, achv_id=1596)
        print(json.dumps(res, indent=4))
        print(f"Total achievement users: {len(res)}")
        return None
    except Exception as error:
        ft_handle_error(error)  # will exit(1)
        return None


if __name__ == "__main__":
    test()
