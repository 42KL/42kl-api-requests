# get_logins_by_cursus.py
"""Get list of user logins registered for a given cursus"""

from FtApi import FtApi
from FtDateTime import is_valid_date
from FtCursus import IDS as CURSUS_IDS, get_cursus_users
from FtUtils import ft_write_error, ft_write_success


def user_input_cursus():
    """Request user input for a Cursus ID"""
    cursus_id = ""
    print("================================================")
    print("ID".rjust(4), end="")
    print(" || Cursus")
    print("==== || ========================================")
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


def user_input_date():
    """Request user input for a date string in YYYY-mm-dd format"""
    date_str = ""
    while not is_valid_date(date_str):
        date_str = input("Enter Cursus BEGIN date in the format YYYY-mm-dd: ")
        if not is_valid_date(date_str):
            ft_write_error(f"{date_str} - Invalid date_str format")
    return date_str

def main():
    """Prints list of user logins registered for a given cursus_id
    beginning on a given BEGIN_DATE to a text file."""
    try:
        CURSUS_ID = user_input_cursus()
        BEGIN_DATE = user_input_date()
        user_data = get_cursus_users(FtApi(), CURSUS_ID, BEGIN_DATE)
        output_filename = f"logins-{CURSUS_ID}-{BEGIN_DATE}.txt"
        with open(output_filename, "w") as OUTPUT_TXT:
            for user in user_data:
                print(user["user"]["login"], file=OUTPUT_TXT)
        message = f"{len(user_data)} logins written to {output_filename}"
        ft_write_success(message)
    except BaseException as error:
        ft_write_error(error)
        exit()
    return


if __name__ == "__main__":
    main()
