# get_logins_by_cursus.py
"""Get list of user logins registered for a given cursus"""

from FtApi import FtApi
from FtCursus import get_cursus_users
from FtInput import read_input_cursus, read_input_date
from FtUtils import ft_write_error, ft_write_success


def get_logins_by_cursus(ft_api: FtApi = None,
                         cursus_id: str = None,
                         begin_date: str = None) -> list():
    """Return a list of user logins for users subscribed to the given
    cursus_id with a begin date within the range of the planned duration."""
    assert ft_api is not None, "Invalid FtApi object."
    assert isinstance(ft_api, FtApi), "Invalid FtApi object."
    assert cursus_id is not None, "cursus_id not specified."
    assert isinstance(cursus_id, str), "cursus_id must be a string."
    if begin_date is not None:
        assert isinstance(begin_date, str), "begin_date must be a string."
    cursus_users = get_cursus_users(ft_api, cursus_id, begin_date)
    logins = [user["user"]["login"] for user in cursus_users]
    return logins


def write_logins_to_file(logins: list() = None, filename: str = None):
    """Prints logins to output file, one login per line."""
    assert logins is not None and len(logins) > 0, \
        "Empty list of logins. No files created."
    assert isinstance(logins, list) and not isinstance(logins, str), \
        "Invalid list of logins given. No files created."
    if filename is None:
        filename = "logins.lst"
    with open(filename, "w") as OUTPUT_TXT:
        for login in logins:
            print(login, file=OUTPUT_TXT)
    message = f"{len(logins)} logins written to {filename}"
    ft_write_success(message)
    return


def main():
    """Prints list of user logins registered for a given cursus_id
    beginning on a given BEGIN_DATE to a text file."""
    try:
        CURSUS_ID = read_input_cursus()
        BEGIN_DATE = read_input_date(allow_null=True)
        LOGINS = get_logins_by_cursus(FtApi(), CURSUS_ID, BEGIN_DATE)
        output_filename = f"logins-{CURSUS_ID}-{BEGIN_DATE}.txt"
        write_logins_to_file(LOGINS, output_filename)
    except BaseException as error:
        ft_write_error(error)
        exit()
    return


if __name__ == "__main__":
    main()
