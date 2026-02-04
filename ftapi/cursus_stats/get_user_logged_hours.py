# get_user_logged_hours.py
"""Summarise user logins over a period of time"""

from io import IOBase
from sys import stdout
from datetime import datetime as dt, timedelta
from time import sleep
from FtApi import FtApi
from utils.ft_datetime import is_valid_date, dt_convert
from FtCursus import DURATION as CURSUS_DURATION, get_cursus_users
from utils.io.ft_input import read_input_cursus, read_input_date
from utils.io.ft_write_stderr import ft_write_error, ft_write_success


def make_attendance_dict(begin_date: str = None, duration: int = 0) -> dict:
    """Build a dictionary with given duration as number of pairs,
    with dates as the keys, one day apart."""
    assert begin_date is not None and isinstance(begin_date, str) and \
        is_valid_date(begin_date), f"{begin_date}: Invalid date."
    assert duration is not None and isinstance(duration, int) and \
        duration > 0, f"{duration}: Invalid duration."
    attendance = dict()
    for day in range(duration):
        date = dt_convert(f"{begin_date}T00:00:00.000Z") + timedelta(days=day)
        attendance[date.strftime("%Y-%m-%d")] = 0
    return attendance


def get_user_locations(ft_api: FtApi = None, login: str = None) -> dict:
    """GET using API locations data for a login"""
    if ft_api is None:
        ft_api = FtApi()
    assert isinstance(ft_api, FtApi), "Invalid API instance."
    assert login is not None, "Invalid login."
    get_url = f"{ft_api.site}/v2/users/{login}/locations"
    return ft_api.get(get_url)


def sum_hours_per_day(location_data: list = None, attendance: dict = None):
    """Calculate and return the total hours per day logged in a given user
    locations data"""
    assert location_data is not None and isinstance(location_data, list) and \
        not isinstance(location_data, str), "Invalid list of locations dict."
    if len(location_data) > 0:
        assert all([isinstance(data, dict) for data in location_data]) and \
            all(["begin_at" in data.keys() for data in location_data]) and \
            all(["end_at" in data.keys() for data in location_data]), \
            "Invalid list of locations dictionary."
    assert attendance is not None and isinstance(attendance, dict) and \
        len(attendance.keys()) > 0 and \
        all([isinstance(key, str) for key in attendance.keys()]) and \
        all(is_valid_date(key) for key in attendance.keys()), \
        "Invalid dictionary of dates."
    for data in location_data:
        log_begin = dt_convert(data["begin_at"])
        log_end = dt_convert(data["end_at"])
        if log_end is None:
            log_end = dt.now() - timedelta(hours=8)
        for date in attendance.keys():
            date_zulu = f"{date}T00:00:00.000Z"
            sum_begin = dt_convert(date_zulu) - timedelta(hours=8)
            sum_end = sum_begin + timedelta(hours=23, minutes=59, seconds=59)
            if log_begin is None:
                continue
            duration = sum_duration_within_range(log_begin, log_end,
                                                 sum_begin, sum_end)
            if duration.days > 0 or duration.seconds > 0:
                attendance[date] += duration.seconds // 3600
                minutes = (duration.seconds % 3600) // 60
                attendance[date] += minutes / 60
    return


def sum_duration_within_range(query_begin: dt = None,
                              query_end: dt = None,
                              target_begin: dt = None,
                              target_end: dt = None) -> dt:
    """Given a query range and a target range, calculate and return the
    duration of overlap."""
    duration = dt.now()
    duration = duration - duration
    if query_end < target_begin or query_begin > target_end:
        return duration
    if query_begin >= target_begin and query_end <= target_end:
        return query_end - query_begin
    if query_begin < target_begin and query_end > target_end:
        return target_end - target_begin
    if query_begin < target_begin and query_end <= target_end:
        return query_end - target_begin
    if query_begin >= target_begin and query_end > target_end:
        return target_end - query_begin
    return duration


def write_attendance_csv_header(attendance: dict = None,
                                file: IOBase = stdout):
    """Print CSV column names for user attendance"""
    assert attendance is not None and isinstance(attendance, dict) and \
        len(attendance.keys()) > 0, "Invalid dictionary of attendance."
    for date in attendance.keys():
        print(f",\"{date}\"", end="", file=file)
    return


def write_attendance_csv_row(login: str = None,
                             attendance: dict = None,
                             file: IOBase = stdout):
    """Print CSV row data for user attendance"""
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "Invalid login."
    assert attendance is not None and isinstance(attendance, dict) and \
        len(attendance.keys()) > 0, "Invalid dictionary of attendance."
    for date in attendance.keys():
        print(f",{attendance[date]:0.2f}", end="", file=file)
    return


def main():
    """Summarise user logins over a period of time
    """
    try:
        ft_api = FtApi()
        CURSUS_ID = read_input_cursus()
        BEGIN_DATE = read_input_date(allow_null=False)
        OUTPUT_FN = "Hours.csv"
        CURSUS_USERS = get_cursus_users(ft_api, CURSUS_ID, BEGIN_DATE)
        LOGINS = [user["user"]["login"] for user in CURSUS_USERS]
        attends = make_attendance_dict(BEGIN_DATE, CURSUS_DURATION[CURSUS_ID])
        with open(OUTPUT_FN, "w") as OUT:
            print("\"login\",\"days\"", end="", file=OUT)
            write_attendance_csv_header(attends, OUT)
            print(file=OUT)
            for login in LOGINS:
                attendance = attends.copy()
                location_data = get_user_locations(ft_api, login)
                sum_hours_per_day(location_data, attendance)
                print(f"{login}", end="", file=OUT)
                hours = [attendance[date] for date in attendance.keys()]
                hours = [x for x in hours if x > 0]
                print(f",{len(hours)}", end="", file=OUT)
                write_attendance_csv_row(login, attendance, OUT)
                print("", file=OUT)
                sleep(0.5)
            OUT.close()
        message = f"Hours for {len(LOGINS)} logins written to {OUTPUT_FN}"
        ft_write_success(message)
    except KeyboardInterrupt:
        print()
        return
    except BaseException as error:
        ft_write_error(f"{type(error)}: {error}")
        exit()
    return


if __name__ == "__main__":
    main()
