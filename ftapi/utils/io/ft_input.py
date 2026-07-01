# ft_input.py
"""Collection of functions to request input"""

from datetime import datetime as dt
from sys import stderr
from FtCursus import IDS as CURSUS_IDS
from utils.ft_datetime import is_valid_date, is_valid_time
from utils.io.ft_write_stderr import ft_puterr_chars, \
                                     ft_puterr_line, \
                                     ft_write_error, \
                                     ft_write_info


def read_input_cursus():
    """Request user input for a Cursus ID"""
    cursus_id = ""
    ft_puterr_line("================================================")
    ft_puterr_line(f"{'ID'.rjust(4)} || Cursus")
    ft_puterr_line("================================================")
    valid_ids = list()
    for cursus in CURSUS_IDS:
        print(f"{str(CURSUS_IDS[cursus]):>4} || {cursus}", file=stderr)
        valid_ids.append(str(CURSUS_IDS[cursus]))
    ft_puterr_line("================================================")
    while cursus_id not in valid_ids:
        ft_puterr_chars("Enter the Cursus ID: ")
        cursus_id = input()
        if cursus_id not in valid_ids:
            ft_write_error(f"{cursus_id} - Unsupported cursus ID")
    return cursus_id


def read_input_date(allow_null: bool = True) -> dt:
    """Request user input for a date string in YYYY-mm-dd format"""
    date_str = ""
    while not is_valid_date(date_str):
        ft_puterr_chars("Enter a date in the format YYYY-mm-dd: ")
        date_str = input()
        if allow_null and len(date_str) == 0:
            ft_write_info("Date not entered, proceed without date.")
            return None
        if not is_valid_date(date_str):
            ft_write_error(f"{date_str} - Invalid date_str format")
    return date_str


def read_input_time(allow_null: bool = True) -> dt:
    """Request user input for a time string in HH:MM format"""
    time_str = ""
    while not is_valid_time(time_str):
        ft_puterr_chars("Enter a time in the format HH:MM: ")
        time_str = input()
        if allow_null and len(time_str) == 0:
            ft_write_info("Time not entered, proceed without time.")
            return None
        if not is_valid_time(time_str):
            ft_write_error(f"{time_str} - Invalid time format")
    return time_str
