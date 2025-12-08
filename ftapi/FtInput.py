# FtInput.py
"""Collection of functions to request input"""

from datetime import datetime as dt
from sys import stderr
from FtDateTime import is_valid_date
from FtCursus import IDS as CURSUS_IDS
from FtUtils import ft_write_error, ft_write_info


def read_input_cursus():
    """Request user input for a Cursus ID"""
    cursus_id = ""
    print("================================================", file=stderr)
    print("ID".rjust(4), end="", file=stderr)
    print(" || Cursus", file=stderr)
    print("================================================", file=stderr)
    valid_ids = list()
    for cursus in CURSUS_IDS:
        print(f"{str(CURSUS_IDS[cursus]):>4} || {cursus}", file=stderr)
        valid_ids.append(str(CURSUS_IDS[cursus]))
    print("================================================", file=stderr)
    while cursus_id not in valid_ids:
        print("Enter the Cursus ID: ", end="", file=stderr)
        cursus_id = input()
        if cursus_id not in valid_ids:
            ft_write_error(f"{cursus_id} - Unsupported cursus ID")
    return cursus_id


def read_input_date(allow_null = True) -> dt:
    """Request user input for a date string in YYYY-mm-dd format"""
    date_str = ""
    while not is_valid_date(date_str):
        print("Enter a date in the format YYYY-mm-dd: ", end="", file=stderr)
        date_str = input()
        if allow_null and len(date_str) == 0:
            ft_write_info(f"Date not entered, proceed without date.")
            return None
        if not is_valid_date(date_str):
            ft_write_error(f"{date_str} - Invalid date_str format")
    return date_str
