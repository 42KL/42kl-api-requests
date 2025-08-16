# FtCursus.py
"""Commonly used cursus constants and functions."""

from datetime import datetime as dt, timedelta
from FtApi import FtApi
from FtDateTime import is_valid_date
from FtUtils import ft_write_info


IDS = {"42": 1,
       "42cursus": 21,
       "c-piscine": 9,
       "c-piscine-brussels": 64,
       "c-piscine-reloaded": 66,
       "discovery-piscine-ai-fundamentals-for-all": 79,
       "discovery-piscine-core-python-programming": 80,
       "discovery-piscine-python": 69,
       "discovery-piscine-web-programming-essentials": 3,
       "piscine-c": 4}
DURATION = {"9": 26, "79": 3, "80": 5, "3": 5}


def get_cursus_users(ft_api: FtApi = None,
                     cursus_id: str = None,
                     begin_date: str = None) -> dict:
    """return a dictionary of user data for user subscribed to the given
    cursus_id with a begin date within the range of the planned duration."""
    if ft_api is None:
        ft_api = FtApi()
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
    if ft_api is None:
        ft_api = FtApi()
    assert isinstance(ft_api, FtApi), "Invalid FtApi object."
    assert cursus_id is not None, "cursus_id not specified."
    assert isinstance(cursus_id, str), "cursus_id must be a string."
    get_url = f"{ft_api.site}/v2/cursus/{cursus_id}/projects"
    ft_write_info(f"GET from {get_url}")
    return ft_api.get(get_url)


def compute_cursus_end_from_begin(cursus_id: str = None,
                                  begin_date: str = None) -> dt:
    """Return cursus end_at from given begin_at based on DURATION constant"""
    if cursus_id is None or not isinstance(cursus_id, str) or \
            cursus_id not in DURATION or \
            begin_date is None or not isinstance(begin_date, str) or \
            not is_valid_date(begin_date):
        return None
    try:
        begin_date = dt.strptime(begin_date, "%Y-%m-%d")
        end_date = begin_date + timedelta(days=DURATION[cursus_id])
        end_date -= timedelta(seconds=1)
        end_date -= timedelta(hours=8)
    except BaseException as error:
        print(error)
        return None
    return str(end_date)

