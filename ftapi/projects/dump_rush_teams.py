# dump_rush_teams.py
"""Dumps Rush Project Teams to text file"""

from dataclasses import dataclass
from FtApi import FtApi
from utils.io.ft_write_stderr import ft_puterr_line, \
                                     ft_write_info, \
                                     ft_write_error


@dataclass
class RushPicker:
    """Data class to help user pick a Rush project"""
    project_id: str
    RUSHES = ["c-piscine-rush-00", "c-piscine-rush-01", "c-piscine-rush-02"]

    def __init__(self, project_id: str = None):
        if project_id is not None and \
                isinstance(project_id, str) and \
                len(project_id) > 0:
            self.project_id = project_id
        else:
            self.project_id = self.read_project_id()

    def __post_init__(self):
        if self.project_id not in self.RUSHES:
            err = "Invalid project_id: " + str(self.project_id) + "."
            raise ValueError(err)

    def __str__(self):
        return self.project_id

    def read_project_id(self):
        picker_index = None
        ft_puterr_line("================================================")
        ft_puterr_line(f"{'ID'.rjust(4)} || Rush Project")
        ft_puterr_line("================================================")
        for i in range(len(self.RUSHES)):
            print(f"{str(i).rjust(4)} || {self.RUSHES[i]}")
        ft_puterr_line("================================================")
        while picker_index is None \
                or picker_index not in range(len(self.RUSHES)):
            picker_index = input("Enter the ID of the Rush project: ")
            try:
                if int(picker_index) not in range(len(self.RUSHES)):
                    ft_write_error(f"Invalid ID: {picker_index}.")
                    picker_index = None
                    continue
                picker_index = int(picker_index)
            except ValueError:
                ft_write_error(f"Invalid input: {picker_index}.")
        ft_write_info("Selected Rush project: " + self.RUSHES[picker_index])
        return self.RUSHES[picker_index]


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
        teams_data = get_rush_teams_by_project(ft_api, str(RushPicker()))
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
