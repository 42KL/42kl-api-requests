# get_user_cursus_results.py
"""Summarise logged hours and final marks for each user in cursus."""

import traceback
from io import IOBase
from sys import stdout
from time import sleep
from FtApi import FtApi
from FtCursus \
    import DURATION as CURSUS_DURATION, get_cursus_users, get_cursus_projects
from FtDateTime import is_valid_date
from FtInput import read_input_cursus, read_input_date
from FtUtils import ft_write_error, ft_write_success
from cursus_stats.get_user_project_finalmarks \
    import get_user_project_finalmarks, \
    write_finalmark_csv_header, write_finalmark_csv_row
from cursus_stats.get_user_logged_hours \
    import make_attendance_dict, get_user_locations, sum_hours_per_day, \
    write_attendance_csv_header, write_attendance_csv_row


def get_cursus_user_login_id_dict(ft_api: FtApi = None,
                                  cursus_id: str = None,
                                  begin_date: str = None) -> dict:
    """GET using API cursus_users for a given cursus_id beginning on given
    begin_date, and summarise and return a dictionary of logins: user_ids."""
    if ft_api is None:
        ft_api = FtApi()
    assert ft_api is not None and isinstance(ft_api, FtApi), \
        "Invalid API instance."
    assert cursus_id is not None and isinstance(cursus_id, str), \
        "Invalid cursus_id."
    assert begin_date is not None and isinstance(begin_date, str) and \
        is_valid_date(begin_date), "Invalid date string."
    CURSUS_USERS = get_cursus_users(ft_api, cursus_id, begin_date)
    logins = dict()
    for user in CURSUS_USERS:
        logins[user["user"]["login"]] = user["user"]["id"]
    return logins


def write_results_csv_header(file: IOBase = stdout,
                             attendance: dict = None,
                             projects: list = None):
    """Prints column names for results table"""
    assert attendance is not None and isinstance(attendance, dict) and \
        all([is_valid_date(key) for key in attendance.keys()]), \
        "Invalid dictionary of attendance."
    assert projects is not None and isinstance(projects, list) and \
        not isinstance(projects, str), "Invalid list of projects."
    print("\"login\",\"days\",\"hours\",\"validated\"", end="", file=file)
    write_attendance_csv_header(file, attendance)
    write_finalmark_csv_header(file, projects)
    print(file=file)
    return


def write_results_csv_row(file: IOBase = stdout,
                          login: str = None, attendance: dict = None,
                          projects: list = None, marks: dict = None):
    """Prints data row for results table"""
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "Invalid login."
    assert attendance is not None and isinstance(attendance, dict) and \
        len(attendance.keys()) > 0, "Invalid dictionary of attendance."
    assert projects is not None and isinstance(projects, list) and \
        not isinstance(projects, str) and len(projects) > 0, \
        "Invalid projects."
    assert marks is not None and isinstance(marks, dict) and \
        "validated?" in marks and "project" in marks and \
        isinstance(marks["project"], dict), "Invalid projects marks data."
    print(login, end="", file=file)
    hours = [attendance[date] for date in attendance.keys()]
    print(f",{len([x for x in hours if x > 0])}", end="", file=file)
    print(f",{sum(hours):0.2f}", end="", file=file)
    print(f",{marks['validated?']}", end="", file=file)
    write_attendance_csv_row(file, login, attendance)
    write_finalmark_csv_row(file, login, projects, marks)
    print(file=file)
    return


def main():
    """Summarise logged hours and final marks for each user in cursus."""
    try:
        ft_api = FtApi()
        CURSUS_ID = read_input_cursus()
        BEGIN_DATE = read_input_date()
        logins = get_cursus_user_login_id_dict(ft_api, CURSUS_ID, BEGIN_DATE)
        attends = make_attendance_dict(BEGIN_DATE, CURSUS_DURATION[CURSUS_ID])
        projects = get_cursus_projects(ft_api, CURSUS_ID)
        OUTPUT_FN = "Results.csv"
        with open(OUTPUT_FN, "w") as OUT:
            write_results_csv_header(OUT, attends, projects)
            for login in logins.keys():
                user_id = logins[login]
                attendance = attends.copy()
                location_data = get_user_locations(ft_api, login)
                sleep(0.5)
                sum_hours_per_day(location_data, attendance)
                marks = get_user_project_finalmarks(ft_api, user_id)
                sleep(0.5)
                write_results_csv_row(OUT, login, attendance, projects, marks)
            OUT.close()
        message = f"Results for {len(logins.keys())} logins "
        message = f"{message} written to {OUTPUT_FN}"
        ft_write_success(message)
    except KeyboardInterrupt:
        print()
        return
    except BaseException:
        ft_write_error(traceback.format_exc())
        return
    return


if __name__ == "__main__":
    main()
