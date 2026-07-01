# get_campus_project_sessions.py

from FtApi import FtApi
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_write_stderr import ft_write_info


def get_campus_project_sessions(ft_api: FtApi = None) -> list:
    """
    GET and PRINT list of projects sessions for campus.
    """
    try:
        if ft_api is None:
            ft_api = FtApi()
        get_url = f"{ft_api.site}/v2/project_sessions"
        get_url = f"{get_url}?filter[campus_id]={ft_api.campus}"
        get_url = f"{get_url}&filter[cursus_id]=21"
        ft_write_info(get_url)
        return ft_api.get(get_url)
    except BaseException:
        raise


if __name__ == "__main__":
    try:
        project_sessions = get_campus_project_sessions()
        print("id,project_id,project name")
        for ps in project_sessions:
            psid = ps['id']
            pid = ps['project_id']
            pn = ps['project']['name']
            cd = ps['created_at']
            psurl = "https://projects.intra.42.fr/projects/"
            psurl = f"{psurl}/{ps['project']['slug']}/"
            psurl = f"{psurl}/project_sessions/{psid}/edit"
            print(f"{psid},{pid},\"{pn}\",\"{cd}\",\"{psurl}\"")
    except BaseException as error:
        ft_handle_error(error)  # will exit(1)
