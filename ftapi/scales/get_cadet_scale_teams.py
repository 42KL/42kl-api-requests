# get_cadet_scale_teams.py
"""Get evaluations (scale teams) for all cadets in campus
from 6 October 2025 to 26 May 2026 (MYT).

Running the script will get evaluations and dump them to a JSON file,
which can be read using json.load into a list of dictionaries."""

from json import dumps as json_dumps
from FtApi import FtApi
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success


def get_cadet_scale_teams(ft_api: FtApi | None = None) -> list[dict]:
    """Get list of evaluations (scale teams) for all cadets in campus.
    This is done by getting all scale teams, filtering for campus_id,
    cursus_id, and filled_at between 6 October 2025 and 26 May 2026.

    Args:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.

    Returns:
        list[dict]: list of evaluations (scale teams) for all cadets in campus.
    """
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    get_url = f"{ft_api.site}/v2/scale_teams"
    get_url += f"?filter[campus_id]={ft_api.campus}"
    get_url += f"&filter[cursus_id]=21"
    get_url += f"&range[filled_at]=2025-10-06T08:00:00Z,2026-05-27T07:59:59Z"
    ft_write_info(f"GET: {get_url}")
    get_res = ft_api.get(get_url)
    ft_write_success("Success!")
    return get_res


if __name__ == "__main__":
    """Print to file called cadet_scale_teams.json the list of evaluations
    (scale teams) for all cadets in campus."""
    with open("cadet_scale_teams.json", "w") as f:
        print(json_dumps(get_cadet_scale_teams(), indent=2), file=f)
