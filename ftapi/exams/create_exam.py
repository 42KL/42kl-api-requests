# create_exam.py
"""Create an exam using the 42 API (v2)."""

import json
from FtApi import FtApi
from exams.FtExam import FtExam
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success


EXAMS = {
    "c-piscine-exam-00": 1301,
    "c-piscine-exam-01": 1302,
    "c-piscine-exam-02": 1303,
    "c-piscine-final-exam": 1304,
    "exam-rank-02": 1320,
    "exam-rank-03": 1321,
    "exam-rank-04": 1322,
    "exam-rank-05": 1323,
    "exam-rank-06": 1324,
    "42next-exam-rank-02": 2708,
    "42next-exam-rank-03": 2709,
    "42next-exam-rank-04": 2710,
    "42next-exam-rank-05": 2711,
    "42next-exam-rank-06": 2712
}


def create_exam(ft_api: FtApi = None,
                exam: FtExam = None) -> list:
    """Create an exam using the 42 API (v2).

    Args:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.
        exam (FtExam): FtExam instance containing exam data to create.
                       Throws warning if not provided.

    Returns:
        list: API response as a list of dictionaries.
    """
    assert exam is not None and isinstance(exam, FtExam), \
        "Exam data must be provided as an FtExam instance. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    post_url = f"{ft_api.site}/v2/exams"
    payload = {"exam": exam.asdict()}
    ft_write_info(f"POST: {post_url} {payload}")
    post_res = ft_api.oauth.post(post_url, json=payload)
    post_res.raise_for_status()
    ft_write_success(f"{exam.name} at {exam.begin_at} created successfully.")
    post_ret = post_res.json()
    post_res.close()
    return post_ret


def test():
    """Test function for create_exam.py."""
    try:
        ft_api = FtApi()
        exam = FtExam(name="Cadet Ranking Exam",
                      begin_at="2026-02-06T06:00:00Z",
                      end_at="2026-02-06T09:00:00Z",
                      location="Cluster 1",
                      ip_range="10.11.0.0/16",
                      campus_id=int(ft_api.campus),
                      activate_waitlist=False,
                      project_ids=[EXAMS["exam-rank-02"],
                                   EXAMS["42next-exam-rank-02"],
                                   EXAMS["42next-exam-rank-03"]])
        exam_creator = create_exam(ft_api=ft_api, exam=exam)
        ft_write_success(json.dumps(exam_creator, indent=4))
    except Exception as err:
        ft_handle_error(err)  # will exit(1)
    return None


if __name__ == "__main__":
    test()
