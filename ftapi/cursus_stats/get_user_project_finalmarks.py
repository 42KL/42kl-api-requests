# get_user_project_finalmarks.py
"""Summarise final marks for each user in cursus."""

from io import IOBase
from sys import stdout
from time import sleep
from FtApi import FtApi
from FtCursus import get_cursus_users, get_cursus_projects
from FtInput import read_input_cursus, read_input_date
from utils.io.ft_write_stderr import ft_write_error, ft_write_success


def get_user_projects(ft_api: FtApi = None, user_id: str = None) -> dict():
    """GET using API projects_users data for given user_id and
    returns as dictionary"""
    if ft_api is None:
        ft_api = FtApi()
    assert isinstance(ft_api, FtApi), "Invalid API instance."
    assert user_id is not None, "Invalid user_id."
    get_url = f"{ft_api.site}/v2/users/{user_id}/projects_users"
    user_projects_data = ft_api.get(get_url)
    return user_projects_data


def get_user_project_finalmarks(ft_api: FtApi = None,
                                user_id: str = None) -> dict():
    """Summarise the final marks for all projects completed by a
    given user_id"""
    if ft_api is None:
        ft_api = FtApi()
    assert isinstance(ft_api, FtApi), "Invalid API instance."
    assert user_id is not None, "Invalid user_id."
    user_projects_data = get_user_projects(ft_api, user_id)
    marks = {"validated?": 0, "project": dict()}
    for proj in user_projects_data:
        if proj["final_mark"] is not None:
            log_mark = proj["final_mark"]
            log_slug = proj["project"]["slug"]
            if log_slug not in marks["project"].keys():
                marks["project"][log_slug] = {"mark": 0, "validated?": False}
            if log_mark > marks["project"][log_slug]["mark"]:
                marks["project"][log_slug]["mark"] = log_mark
                marks["project"][log_slug]["validated?"] = proj["validated?"]
                if proj["validated?"] is True:
                    marks["validated?"] += 1
    return marks


def write_finalmark_csv_header(projects: list = None, file: IOBase = stdout):
    """Print CSV column names for user finalmarks"""
    assert projects is not None and isinstance(projects, list) and \
        not isinstance(projects, str), "Invalid list of project names."
    for project in projects:
        print(f",\"{project['slug']}\"", end="", file=file)
    for project in projects:
        print(f",\"{project['slug']} validated?\"", end="", file=file)
    return


def write_finalmark_csv_row(login: str = None,
                            projects: list = None,
                            marks: dict = None,
                            file: IOBase = stdout):
    """Print CSV row data for user finalmarks"""
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "Invalid login."
    assert projects is not None and isinstance(projects, list) and \
        not isinstance(projects, str) and len(projects) > 0, \
        "Invalid projects."
    assert marks is not None and isinstance(marks, dict) and \
        "validated?" in marks and "project" in marks and \
        isinstance(marks["project"], dict), "Invalid projects marks data."
    for project in projects:
        slug = project["slug"]
        mark = 0
        if slug in marks['project']:
            mark = marks['project'][slug]['mark']
        print(f",{mark}", end="", file=file)
    for project in projects:
        slug = project["slug"]
        stat = False
        if slug in marks['project']:
            stat = marks['project'][slug]['validated?']
        print(f",{stat}", end="", file=file)
    return


def main():
    """Summarise final marks for each user in cursus."""
    try:
        ft_api = FtApi()
        CURSUS_ID = read_input_cursus()
        START_DATE = read_input_date(allow_null=True)
        OUTPUT_FN = "Finalmarks.csv"
        projects = get_cursus_projects(ft_api, CURSUS_ID)
        users = get_cursus_users(ft_api, CURSUS_ID, START_DATE)
        logins = dict()
        for user in users:
            logins[user["user"]["login"]] = user["user"]["id"]
        with open(OUTPUT_FN, "w") as OUT:
            print("\"login\",\"validated\"", end="", file=OUT)
            write_finalmark_csv_header(projects, OUT)
            print(file=OUT)
            for login in logins.keys():
                user_id = logins[login]
                marks = get_user_project_finalmarks(ft_api, user_id)
                print(f"{login},{marks['validated?']}", end="", file=OUT)
                write_finalmark_csv_row(login, projects, marks, OUT)
                print(file=OUT)
                sleep(0.5)
            OUT.close()
        message = f"Final marks for {len(logins.keys())} logins"
        message = f"{message} written to {OUTPUT_FN}"
        ft_write_success(message)
    except BaseException as error:
        ft_write_error(f"{str(type(error))}: {error}")
        exit()

    return


if __name__ == "__main__":
    main()
