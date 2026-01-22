# ft_read_file.py
"""Collection of methods to systematically read input from files."""


import json


def ft_read_list(file_path: str) -> list:
    """Reads a file, store each line of characters as a string
    in a list, and returns the list.

    Attributes:
        file_path (str): Path to the file to read

    Returns:
        list: List of strings, one from each line in the given file.
    """
    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    lines.append(line)
    except Exception:
        raise
    return lines


def test(file_path: str = "ft_read_file_test_input.txt") -> None:
    """Test function for ft_read_file method.

    Attributes:
        file_path (str): Path to the file to read
                         Defaults to using "ft_read_file_test_input.txt"
    """
    lines = ft_read_list(file_path=file_path)
    if lines:
        print(json.dumps(lines, indent=4))
    return


if __name__ == "__main__":
    test()
