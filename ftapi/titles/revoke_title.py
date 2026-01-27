# revoke_title.py
"""Revoke a title from a user using 42 API (v2)."""

from FtApi import FtApi
from FtUtils import ft_write_error, ft_write_info, ft_write_success


def revoke_title(ft_api: FtApi = None,
                 title_user_id: int = None) -> None:
    """Revoke a title from a user using 42 API (v2).

    Args:
        ft_api (FtApi): An FtApi instance (42 API authentication object).
                        Optional, instantiated if note provided.
        title_user_id (int): ID of the title user record to DELETE.
    """
    assert title_user_id is not None and isinstance(title_user_id, int), \
        "Title user ID must be given as a non-empty integer. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    delete_url = f"{ft_api.site}/v2/titles_users/{title_user_id}"
    ft_write_info(f"DELETE {delete_url}")
    delete_res = ft_api.oauth.delete(delete_url)
    delete_res.raise_for_status()
    ft_write_success(f"Title revoked for titles_users record {title_user_id}.")
    delete_res.close()
    return None


def test() -> None:
    """Test revoke_title function.
    Revokes the title user record with ID 53638 as an example.
    """
    try:
        ft_api = FtApi()
        revoke_title(ft_api=ft_api, title_user_id=53638)
        return None
    except Exception as error:
        ft_write_error(error)
        return None


if __name__ == "__main__":
    test()
