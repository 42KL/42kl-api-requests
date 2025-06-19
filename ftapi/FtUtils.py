# utils.py
"""Commonly used handy little utility functions."""

import colorama
import sys


def ft_write_error(message: str):
    """Writes messages to the screen (stderr) using red font."""
    colorama.init(autoreset=True)
    print(f"{colorama.Fore.RED}{message}", file=sys.stderr)
    return


def ft_write_info(message: str):
    """Writes messages to the screen (stderr) using yellow font."""
    colorama.init(autoreset=True)
    print(f"{colorama.Fore.YELLOW}[INFO] {message}", file=sys.stderr)
    return


def ft_write_success(message: str):
    """Writes messages to the screen (stderr) using green font."""
    colorama.init(autoreset=True)
    print(f"{colorama.Fore.GREEN}[SUCCESS] {message}", file=sys.stderr)
    return
