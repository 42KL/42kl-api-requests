# summarise_cadet_evals.py
"""Summarise cadet evaluations."""

from json import dumps as json_dumps, load as json_load
from scales.get_cadet_scale_teams import get_cadet_scale_teams
from utils.io.ft_read_file import ft_read_list


def summarise_cadet_evals(login: str | None = None,
                          cadet_scale_teams: list | None = None) -> str:
    """Summarise number of evaluations (scale teams) for a given login,
    as corrector and as corrected, in CSV format.

    Args:
        login: The 42 intra login to summarise.
        cadet_scale_teams: A list of scale teams.

    Returns:
        A string containing the login and the number of evaluations,
        as corrector and corrected, in CSV format.
    """
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "42 intra login must be given as a non-empty string. Nothing is done."
    assert cadet_scale_teams is not None and \
        isinstance(cadet_scale_teams, list) and \
        len(cadet_scale_teams) > 0 and \
        all(isinstance(item, dict) for item in cadet_scale_teams) and \
        all("id" in item.keys() for item in cadet_scale_teams), \
        "Unexpected data structure for cadet scale teams. Nothing is done."
    corrector_scale_ids = set()
    corrected_scale_ids = set()
    for team in cadet_scale_teams:
        # Skip non-unique evaluations
        if team["id"] in corrector_scale_ids or \
                team["id"] in corrected_scale_ids:
            continue
        # correcteds can be a list of multiple users,
        # but corrector is always a single user.
        # When corrector/correcteds are not dict/list of dicts,
        # the evaluation was cancelled/never filled, so skip it.
        correcteds = team["correcteds"]
        if not isinstance(team["corrector"], dict) or \
                not isinstance(correcteds, list) or \
                not all(isinstance(x, dict) for x in correcteds):
            continue
        correcteds = [corrected["login"] for corrected in team["correcteds"]]
        # a user is either a corrector or a corrected in an evaluation,
        # in either case, track the evaluation by id to skip duplicates,
        # if neither, don't do anything.
        if team["corrector"]["login"] == login:
            corrector_scale_ids.add(team["id"])
        elif login in correcteds:
            corrected_scale_ids.add(team["id"])
    # Return the data as a CSV string, allowing user to decide how to write it.
    return (f"{login},{len(corrector_scale_ids)},{len(corrected_scale_ids)}")


if __name__ == "__main__":
    """From a list of evaluations (scale teams) and a list of logins,
    check the number of evaluations each login is a corrector or
    one of the corrected, and write the results in a CSV format."""
    cadet_scale_teams = None
    # Get list of evaluations
    # If the cadet_scale_teams.json file exists, read from it.
    # Otherwise, get the data from the API (and save it to file).
    try:
        with open("cadet_scale_teams.json", "r") as f:
            cadet_scale_teams = json_load(f)
    except FileNotFoundError:
        cadet_scale_teams = get_cadet_scale_teams()
        with open("cadet_scale_teams.json", "w") as f:
            print(json_dumps(cadet_scale_teams, indent=2), file=f)
    except Exception:
        raise
    # Stop further processing if the data is not in the expected format.
    assert cadet_scale_teams is not None and \
        isinstance(cadet_scale_teams, list) and \
        len(cadet_scale_teams) > 0 and \
        all(isinstance(item, dict) for item in cadet_scale_teams) and \
        all("id" in item.keys() for item in cadet_scale_teams), \
        "Problem getting cadet scale teams. Nothing further is done."
    # Get list of logins
    logins = ft_read_list("cadets.lst")
    # Stop further processing if the data is not in the expected format.
    assert logins is not None and isinstance(logins, list) and \
        len(logins) > 0 and all(isinstance(item, str) for item in logins) and \
        all(len(item) > 0 for item in logins), \
        "Problem getting logins. Nothing further is done."
    with open("cadet_evals_summary.csv", "w") as f:
        print("login,corrector,corrected", file=f)
        for login in logins:
            print(summarise_cadet_evals(login, cadet_scale_teams), file=f)
