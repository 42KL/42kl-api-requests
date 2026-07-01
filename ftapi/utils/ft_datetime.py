# ft_datetime.py
"""Useful datetime functions that are reused often"""

from datetime import datetime as dt
import re


def is_valid_date(date_string: str = None):
    """returns True if the given date_string is a valid date string
    conforming to the format YYYY-mm-dd"""
    assert date_string is not None, f"{date_string}: Invalid date string."
    assert isinstance(date_string, str), f"{date_string}: Invalid date string."
    dt_object = None
    try:
        dt_object = dt.strptime(date_string, "%Y-%m-%d")
    except BaseException:
        return False
    assert dt_object is not None, f"{date_string}: Invalid date string."
    return True


def is_valid_time(time_string: str = None):
    """returns True if the given time_string is a valid time string
    conforming to the format HH:MM"""
    assert time_string is not None, f"{time_string}: Invalid time string."
    assert isinstance(time_string, str), f"{time_string}: Invalid time string."
    dt_object = None
    try:
        dt_object = dt.strptime(time_string, "%H:%M")
    except BaseException:
        return False
    assert dt_object is not None, f"{time_string}: Invalid time string."
    return True


def dt_convert(iso_time_string: str):
    """Convert an isoformat date time string back to date time object
    """
    if iso_time_string is None or not isinstance(iso_time_string, str):
        return None
    dt_object = None
    try:        
        zulu_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{1,6}Z"
        zulu_regex = re.compile(zulu_regex)
        if re.fullmatch(zulu_regex, iso_time_string):
            dt_object = dt.strptime(iso_time_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            dt_object = dt.fromisoformat(iso_time_string)
    except BaseException:
        raise
    return dt_object
