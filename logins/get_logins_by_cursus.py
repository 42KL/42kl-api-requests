# get_logins_by_cursus.py
"""Get list of user logins registered for a given cursus"""

from FtApi import FtApi
from FtCursus import get_cursus_users
from FtInput import read_input_cursus, read_input_date
from FtUtils import ft_write_error, ft_write_success


def main():
    """Prints list of user logins registered for a given cursus_id
    beginning on a given BEGIN_DATE to a text file."""
    try:
        CURSUS_ID = read_input_cursus()
        BEGIN_DATE = read_input_date()
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
