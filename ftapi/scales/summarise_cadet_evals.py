# summarise_cadet_evals.py
"""Summarise cadet evaluations."""

from json import dumps as json_dumps
from FtApi import FtApi
from users.get_user_id_by_login import get_user_id_by_login
from utils.io.ft_read_file import ft_read_list
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success


def get_cadet_scale_teams(ft_api: FtApi | None = None,
                          login: str | None = None) -> list[dict]:
    """Get list of evaluations (scale teams) for all cadets in campus.
    This is done by getting all scale teams, filtering for campus_id
    and cursus_id.

    Args:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.
        login (str): 42 intra login of a user to get data for.

    Returns:
        list[dict]: list of evaluations (scale teams) for all cadets in campus.
    """
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "42 intra login must be given as a non-empty string. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    user_id = get_user_id_by_login(ft_api=ft_api, login=login)
    get_url = f"{ft_api.site}/v2/users/{user_id}/scale_teams"
    get_url += f"?filter[campus_id]={ft_api.campus}"
    get_url += f"&filter[cursus_id]=21"
    get_url += f"&range[filled_at]=2025-10-06T08:00:00Z,2026-05-27T07:59:59Z"
    ft_write_info(f"GET: {get_url}")
    get_res = ft_api.get(get_url)
    ft_write_success("Success!")
    return get_res


def summarise_cadet_scale_teams(login: str | None = None) -> str:
    """Summarise number of evaluations (scale teams) for a given login,
    as corrector and as corrected."""
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "42 intra login must be given as a non-empty string. Nothing is done."
    corrector_scale_ids = set()
    corrected_scale_ids = set()
    cadet_scale_teams = get_cadet_scale_teams(login=login)
    for team in cadet_scale_teams:
        if team["id"] in corrector_scale_ids or \
                team["id"] in corrected_scale_ids:
            continue
        correcteds = team["correcteds"]
        if not isinstance(team["corrector"], dict) or \
                not isinstance(correcteds, list) or \
                not all(isinstance(x, dict) for x in correcteds):
            continue
        correcteds = [corrected["login"] for corrected in team["correcteds"]]
        if team["corrector"]["login"] == login:
            corrector_scale_ids.add(team["id"])
        elif login in correcteds:
            corrected_scale_ids.add(team["id"])
    return (f"{login},{len(corrector_scale_ids)},{len(corrected_scale_ids)}")


if __name__ == "__main__":
    """Read a list of logins from a file and print the summary of evaluations
    for each login in CSV format."""
    logins = ft_read_list("cadets.lst")
    with open("cadet_evals_summary.csv", "w") as file:
        print("login,corrector,corrected", file=file)
        for login in logins:
            print(summarise_cadet_scale_teams(login=login), file=file)
