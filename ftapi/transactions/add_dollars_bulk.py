# add_dollars_bulk.py
"""Adds Alterian dollars to users in bulk by reading data from a CSV file."""

from sys import argv
from FtApi import FtApi
from transactions.add_dollars import add_dollars
from utils.io.ft_read_csv import read_csv_into_list
from utils.io.ft_handle_error import ft_handle_error


def add_dollars_bulk(filename: str = None) -> None:
    """Adds Alterian dollars to users in bulk by reading data from a CSV file.

    Attributes:
        filename (str): Path to CSV file containing user data, including
                        login, amount, and reason for each transaction.
    """
    assert filename is not None and \
        isinstance(filename, str) and \
        len(filename) > 0, \
        "Filename must be a non-empty string."
    try:
        csv_data = read_csv_into_list(filename=filename)
        ft_api = FtApi()
        for [login, amount, reason] in csv_data:
            if login.strip().lower() == "login":
                continue
            add_dollars(ft_api=ft_api,
                        login=login,
                        amount=int(amount),
                        reason=reason)
    except BaseException as error:
        ft_handle_error(error)
        return
    return


def main():
    """Adds dollars to users in bulk by reading data from a CSV file given as
    a command line argument (required)."""
    USAGE = f"USAGE: python3 {argv[0]} transactions.csv"
    USAGE += """
    transactions.csv: CSV file containing transaction data,
                      one transaction per line, with login, amount, and reason
                      on each line, separated by commas.
                      Recommended header line: "login,amount,reason"."""
    try:
        if len(argv) != 2:
            raise Exception(f"Missing data file. \n{USAGE}")
            return
        filename = argv[1]
        add_dollars_bulk(filename=filename)
    except BaseException as error:
        ft_handle_error(error)
        return
    return


if __name__ == "__main__":
    main()
