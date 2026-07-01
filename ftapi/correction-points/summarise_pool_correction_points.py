# summarise_pool_correction_points.py
"""Summarise the correction points in the pool."""

import sys
from FtApi import FtApi
from FtCursus import get_cursus_users
from utils.io.ft_input import read_input_cursus, read_input_date
from utils.io.ft_write_stderr import ft_write_error


def summarise_pool_correction_points(user_data: list, out=sys.stdout):
    """From GET response for cursus_users, summarise user correction point
    in a CSV format table."""
    assert isinstance(user_data, list) and \
        isinstance(user_data[0], dict) and \
        "user" in user_data[0].keys() and \
        "login" in user_data[0]["user"].keys() and \
        "correction_point" in user_data[0]["user"].keys(), \
        "Invalid GET response for cursus_users"
    print("\"Login\",\"Correction Point\"", file=out)
    for user in user_data:
        print(f"\"{user['user']['login']}\"", end="", file=out)
        print(f",{user['user']['correction_point']}", file=out)
    return


def main():
    """Prints correction points summary to file."""
    try:
        ft_api = FtApi()
        CURSUS_ID = read_input_cursus()
        CURSUS_BEGIN = read_input_date()
        user_data = get_cursus_users(ft_api, CURSUS_ID, CURSUS_BEGIN)
        assert user_data is not None and len(user_data) > 0, \
            "GET data empty, check CURSUS_ID or CURSUS_BEGIN."
        with open("correction_points.csv", "w") as output_csv:
            summarise_pool_correction_points(user_data, output_csv)
            output_csv.close()
    except AssertionError as error:
        ft_write_error(f"AssertionError: {error}")
        exit()
    except BaseException as error:
        ft_write_error(error)
        exit()
    return


if __name__ == "__main__":
    main()
