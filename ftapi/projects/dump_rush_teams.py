# dump_rush_teams.py
"""Dumps Rush Project Teams to text file"""

import json
import sys
sys.path.append("ftapi")
from FtApi import FtApi
from FtUtils import ft_write_error


def get_rush_teams_by_project(ft_api: FtApi, project_id: str):
    """GET teams from 42 API and returns request object"""
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    get_url = f"{ft_api.site}/v2/projects/{project_id}/teams"
    get_url = f"{get_url}?filter[campus]={ft_api.campus}"
    get_url = f"{get_url}&filter[status]=in_progress"
    return ft_api.get(get_url)


def main():
    try:
        ft_api = FtApi()
        teams_data = get_rush_teams_by_project(ft_api, "c-piscine-rush-00")
        assert len(teams_data) > 0, "No teams fetched"
        print("Leader", "\t", "Members", sep="")
        for team in teams_data:
            leader = None
            logins = []
            for user in team["users"]:
                if user["leader"] is True:
                    leader = user["login"]
                else:
                    logins.append(user["login"])
            print(leader, "\t", leader, ",", ",".join(logins), sep="")
    except BaseException as error:
        ft_write_error(error)
        exit()
    return


if __name__ == "__main__":
    main()
