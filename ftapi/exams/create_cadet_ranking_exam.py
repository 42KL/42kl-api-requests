# create_cadet_ranking_exam.py
"""Create a Cadet Ranking Exam using the 42 API (v2).

A typical Cadet Ranking Exam has the following constants:
- name: Cadet Ranking Exam
- duration: 3 hours
- location: Cluster 1
- ip_range: 10.11.0.0/16"""

from datetime import timedelta
import json
import sys
from FtApi import FtApi
from exams.FtExam import FtExam
from exams.create_exam import EXAMS, create_exam
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_input import read_input_date, read_input_time
from utils.io.ft_write_stderr import ft_write_info, ft_write_success
from utils.ft_datetime import dt_convert


EXAM_NAME = "Cadet Ranking Exam"
EXAM_DURATION = 3  # hours
EXAM_LOC = "Cluster 1"  # Typical location for Cadet Ranking Exams
EXAM_IP_RANGE = "10.11.0.0/16"  # Typical IP range for Cadet Ranking Exams
EXAM_PROJECTS = [
    EXAMS["exam-rank-02"],
    EXAMS["42next-exam-rank-02"],
    EXAMS["42next-exam-rank-03"],
    EXAMS["42next-exam-rank-04"],
    EXAMS["42next-exam-rank-05"],
    EXAMS["42next-exam-rank-06"]
]


def create_cadet_ranking_exam():
    """Module to create Cadet Ranking Exam using the 42 API (v2).

    Module checks if a date and time is provided via command line arguments,
    otherwise prompts the user for input.
    """
    try:
        if sys.argv.__len__() < 3:
            USAGE = f"Usage: {sys.argv[0]} <exam_date> <exam_time>"
            USAGE += "\n    Exam date and time not provided via command line."
            USAGE += "\n    Input after the prompts or press Ctrl+D to quit."
            ft_write_info(USAGE)
            BEGIN_DATE = read_input_date(allow_null=False)
            BEGIN_TIME = read_input_time(allow_null=False)
        elif sys.argv.__len__() == 3:
            BEGIN_DATE = sys.argv[1].strip()
            BEGIN_TIME = sys.argv[2].strip()
        else:
            raise Exception(f"Too many arguments provided.\n{USAGE}")
        ft_api = FtApi()
        BEGIN_AT = dt_convert(f"{BEGIN_DATE} {BEGIN_TIME}+08:00")
        END_AT = BEGIN_AT + timedelta(hours=3)
        exam = FtExam(name=EXAM_NAME,
                      begin_at=BEGIN_AT.isoformat(),
                      end_at=END_AT.isoformat(),
                      location=EXAM_LOC,
                      ip_range=EXAM_IP_RANGE,
                      campus_id=int(ft_api.campus),
                      project_ids=EXAM_PROJECTS)
        exam_creator = create_exam(ft_api=ft_api, exam=exam)
        ft_write_success(json.dumps(exam_creator, indent=4))
    except BaseException as err:
        ft_handle_error(err)  # will exit(1)
    return None


if __name__ == "__main__":
    create_cadet_ranking_exam()
