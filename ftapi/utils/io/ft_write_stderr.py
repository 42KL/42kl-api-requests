# ft_write_stderr.py
"""Reusable modules to print messages to stderr."""

from sys import stderr


def ft_puterr_chars(message: str):
    """Writes messages to the screen (stderr) in default format,
    without a newline character at the end."""
    print(message, end="", file=stderr)
    return


def ft_puterr_line(message: str):
    """Writes messages to the screen (stderr) in default format."""
    print(message, file=stderr)
    return


def ft_write_error(message: str):
    """Writes messages to the screen (stderr) using red font."""
    print(f"\033[31m{message}\033[0m", file=stderr)
    return


def ft_write_info(message: str):
    """Writes messages to the screen (stderr) using yellow font."""
    print(f"\033[33m[INFO] {message}\033[0m", file=stderr)
    return


def ft_write_success(message: str):
    """Writes messages to the screen (stderr) using green font."""
    print(f"\033[32m[SUCCESS] {message}\033[0m", file=stderr)
    return
