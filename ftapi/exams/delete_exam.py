# delete_exam.py
"""Delete an exam using the 42 API (v2)."""

import sys
from FtApi import FtApi
from utils.io.ft_write_stderr import ft_write_error, \
                                     ft_write_info, \
                                     ft_write_success


def delete_exam(ft_api: FtApi = None,
                exam_id: int = None) -> None:
    """Delete an exam using the 42 API (v2).

    Args:
        ft_api (FtApi): FtApi instance (42 API authentication object, optional)
                        Instantiated if not provided.
        exam_id (int): ID of the exam to delete.

    Returns:
        None
    """
    assert exam_id is not None and isinstance(exam_id, int), \
        "Exam ID must be provided as an integer. Nothing is done."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    delete_url = f"{ft_api.site}/v2/exams/{exam_id}"
    ft_write_info(f"DELETE: {delete_url}")
    delete_res = ft_api.oauth.delete(delete_url)
    delete_res.raise_for_status()
    ft_write_success(f"Exam ID {exam_id} deleted successfully.")
    delete_res.close()
    return


def main():
    """Main function for delete_exam.py.
    Checks if an exam ID is given as a command line argument,
    and asks for it to be entered interactively if not.
    Then, deletes the exam with the given ID."""
    USAGE = f"USAGE:\n    python3 {sys.argv[0]} [exam_id]"
    USAGE += "\n"
    USAGE += "    exam_id: (Optional) ID of the exam to delete."
    try:
        if sys.argv.__len__() < 2:
            exam_id = input("Enter ID of exam to delete: ")
        elif sys.argv.__len__() == 2:
            exam_id = sys.argv[1]
        else:
            raise Exception(f"Too many arguments provided.\n{USAGE}")
        ft_api = FtApi()
        exam_id = int(exam_id.strip())
        delete_exam(ft_api=ft_api, exam_id=exam_id)
    except BaseException as err:
        err_msg = "ERROR: "
        if f"{type(err).__name__}" != "Exception":
            err_msg += f"{type(err).__name__}:\n"
        if len(f"{err}") > 0:
            err_msg += f"{err}"
        ft_write_error(err_msg)
        exit(1)
    return None


if __name__ == "__main__":
    main()
