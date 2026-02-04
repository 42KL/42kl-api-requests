# ft_handle_error.py
"""Default error handling module for FtApi."""

from utils.io.ft_write_stderr import ft_write_error


def ft_handle_error(err: BaseException) -> None:
    """Default error handling module for FtApi.
    Prints to stderr an error message containing error type and message.

    Args:
        err (BaseException): The exception to handle.

    Returns:
        None
    """
    err_msg = "ERROR: "
    if f"{type(err).__name__}" != "Exception":
        err_msg += f"{type(err).__name__}:\n"
    if len(f"{err}") > 0:
        err_msg += f"{err}"
    ft_write_error(err_msg)
    exit(1)
    return None
