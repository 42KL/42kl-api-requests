# get_titles_users_by_id.py
"""Get titles users for a given title ID using 42 API (v2)."""

import json
from FtApi import FtApi
from utils.io.ft_write_stderr import ft_write_error, ft_write_info


def get_titles_users_by_id(ft_api: FtApi = None,
                           title_id: int = None) -> list:
    """Get titles users for a given title ID using 42 API (v2).

    Args:
        ft_api (FtApi): An FtApi instance (42 API authentication object).
                        Optional, instantiated if note provided.
        title_id (int): ID of the title to GET users for.

    Returns:
        list: A list of title user dictionaries.
    """
    assert title_id is not None and isinstance(title_id, int), \
        "Title ID must be given as a non-empty integer. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    get_url = f"{ft_api.site}/v2/titles/{title_id}"
    get_url += "/titles_users"
    ft_write_info(f"GET {get_url}")
    return ft_api.get(get_url)


def test() -> None:
    """Test get_titles_users_by_id function.
    Gets and dumps title users for title ID 2655,
    which is the "42IP Mission Commander" title.
    """
    try:
        ft_api = FtApi()
        res = get_titles_users_by_id(ft_api=ft_api, title_id=2655)
        print(json.dumps(res, indent=4))
        print(f"Total title users: {len(res)}")
        return None
    except Exception as error:
        ft_write_error(error)
        return None


if __name__ == "__main__":
    test()
