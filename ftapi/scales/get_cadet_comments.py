# get_cadet_comments.py
"""Analyse a list of evaluations (scale teams), and summarise comments/feedback
made by/given by a given cadet (login)."""

from json import dumps as json_dumps, load as json_load
from pathlib import Path
from scales.get_cadet_scale_teams import get_cadet_scale_teams
from utils.io.ft_read_file import ft_read_list


def get_cadet_comments(login: str | None = None,
                       cadet_scale_teams: list | None = None) -> str:
    """Get comments/feedback made by/given by a given cadet (login).

    Args:
        login: The 42 intra login to summarise.
        cadet_scale_teams: A list of scale teams.

    Returns:
        A string containing the comments/feedback made by/given by the cadet
        with the given login.
    """
    assert login is not None and isinstance(login, str) and len(login) > 0, \
        "42 intra login must be given as a non-empty string. Nothing is done."
    assert cadet_scale_teams is not None and \
        isinstance(cadet_scale_teams, list) and \
        len(cadet_scale_teams) > 0 and \
        all(isinstance(item, dict) for item in cadet_scale_teams) and \
        all("id" in item.keys() for item in cadet_scale_teams), \
        "Unexpected data structure for cadet scale teams. Nothing is done."
    scale_ids = set()
    # cadet comments is a string of all comments/feedback involving the cadet
    # in the following format:
    # - evaluation id:
    #   - corrector:
    #     - comment line 1
    #     - comment line 2
    #     - ...
    #   - correcteds:
    #     - feedback line 1
    #     - feedback line 2
    #     - ...
    cadet_comments = ""
    for team in cadet_scale_teams:
        # Skip non-unique evaluations
        if team["id"] in scale_ids:
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
        # team_comment is the comment made by the corrector, and
        # team_feedback is the feedback made by the correcteds.
        # Normalise the comment and feedback strings,
        # use \n for newlines, and strip whitespaces from both ends.
        team_comment = team["comment"].replace("\r", "\n").strip()
        team_feedback = team["feedback"].replace("\r", "\n").strip()
        # a user is either a corrector or a corrected in an evaluation,
        # in either case, track the evaluation by id to skip duplicates,
        # if neither, don't do anything.
        if team["corrector"]["login"] == login or login in correcteds:
            cadet_comments += f"- {team['id']}:\n"
            if len(team_comment) > 0:
                cadet_comments += f"  - {team['corrector']['login']}:\n"
                for comment_line in team_comment.splitlines():
                    cadet_comments += f"    - {comment_line.strip()}\n"
            if len(team_feedback) > 0:
                cadet_comments += f"  - {','.join(correcteds)}:\n"
                for feedback_line in team_feedback.splitlines():
                    cadet_comments += f"    - {feedback_line.strip()}\n"
            scale_ids.add(team["id"])
    return cadet_comments


if __name__ == "__main__":
    """From a list of evaluations (scale teams) and a list of logins,
    get the comments/feedbacks made by/given by each login."""
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
    # Ensure the directory to write the files exists.
    Path("cadet_comments").mkdir(exist_ok=True)
    for login in logins:
        with open(f"cadet_comments/{login}.yml", "w") as f:
            print(get_cadet_comments(login, cadet_scale_teams), file=f)
