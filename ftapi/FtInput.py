# FtInput.py
"""Collection of functions to request input"""

from datetime import datetime as dt
from FtDateTime import is_valid_date
from FtCursus import IDS as CURSUS_IDS
from FtUtils import ft_write_error


def read_input_cursus():
    """Request user input for a Cursus ID"""
    cursus_id = ""
    print("================================================")
    print("ID".rjust(4), end="")
    print(" || Cursus")
    print("================================================")
    valid_ids = list()
    for cursus in CURSUS_IDS:
        print(f"{str(CURSUS_IDS[cursus]):>4} || {cursus}")
        valid_ids.append(str(CURSUS_IDS[cursus]))
    print("================================================")
    while cursus_id not in valid_ids:
        cursus_id = input("Enter the Cursus ID: ")
        if cursus_id not in valid_ids:
            ft_write_error(f"{cursus_id} - Unsupported cursus ID")
    return cursus_id


def read_input_date() -> dt:
    """Request user input for a date string in YYYY-mm-dd format"""
    date_str = ""
    while not is_valid_date(date_str):
        date_str = input(f"Enter a date in the format YYYY-mm-dd: ")
        if not is_valid_date(date_str):
            ft_write_error(f"{date_str} - Invalid date_str format")
    return date_str
