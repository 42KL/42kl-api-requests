# FtCursus.py
"""Commonly used cursus constants and functions."""

from datetime import datetime as dt, timedelta
from FtApi import FtApi
from FtUtils import ft_write_info


IDS = {"c-piscine": 9,
       "disco-piscine-ai": 79,
       "disco-piscine-python": 80}
DURATION = {"9": 26, "80": 5, "79": 3}


def get_cursus_users(ft_api: FtApi = None,
                     cursus_id: str = None,
                     begin_date: str = None) -> dict:
    """return a dictionary of user data for user subscribed to the given
    cursus_id with a begin date within the range of the planned duration."""
    assert ft_api is not None, "Invalid FtApi object."
    assert isinstance(ft_api, FtApi), "Invalid FtApi object."
    assert cursus_id is not None, "cursus_id not specified."
    assert isinstance(cursus_id, str), "cursus_id must be a string."
    if begin_date is not None:
        assert isinstance(begin_date, str), "begin_date must be a string."
    get_url = f"{ft_api.site}/v2/cursus/{cursus_id}/cursus_users"
    get_url = f"{get_url}?filter[campus_id]={ft_api.campus}"
    if begin_date is not None:
        try:
            begin_date = dt.strptime(begin_date, "%Y-%m-%d")
            begin_date -= timedelta(hours=8)
            end_date = begin_date + timedelta(days=DURATION[cursus_id])
            end_date -= timedelta(seconds=1)
        except BaseException as error:
            raise error
            return None
        get_url = f"{get_url}&range[begin_at]={begin_date},{end_date}"
    get_url = f"{get_url}&sort=created_at"
    ft_write_info(f"GET from {get_url}")
    return ft_api.get(get_url)


def get_cursus_projects(ft_api: FtApi = None,
                        cursus_id: str = None) -> dict:
    """return a dictionary of project data for projects in given cursus."""
    assert ft_api is not None and isinstance(ft_api, FtApi), \
        "Invalid FtApi object."
    assert cursus_id is not None, "cursus_id not specified."
    assert isinstance(cursus_id, str), "cursus_id must be a string."
    get_url = f"{ft_api.site}/v2/cursus/{cursus_id}/projects"
    ft_write_info(f"GET from {get_url}")
    return ft_api.get(get_url)
