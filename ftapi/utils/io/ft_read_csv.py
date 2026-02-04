# ft_read_csv.py
"""A collection of functions used with CSV file input"""

import csv


def read_csv_into_list(filename: str = None):
    """Read given CSV filename and return list of rows."""
    assert filename is not None, "CSV Filename not specified"
    csv_data = list()
    try:
        with open(filename) as CSV_FILE:
            read_buffer = csv.reader(CSV_FILE)
            for row in read_buffer:
                csv_data.append(row)
            CSV_FILE.close()
    except BaseException as error:
        raise error
    assert len(csv_data) > 0, f"No data read from {filename}"
    return csv_data


def get_index(target: str = None, source: list = None):
    """Find and return the index of a string in a list of strings."""
    assert target is not None, "Target string not defined"
    assert source is not None, "Source strings not defined"
    assert isinstance(target, str), "Target is not a string"
    assert isinstance(source, list) and not isinstance(source, str), \
        "Source is not a list of strings"
    i = 0
    while source[i] != target:
        i += 1
    return i
