# generate_password.py
"""Generates random passwords of a given length."""

import secrets
import string


def generate_password(length: int = 12) -> str:
    """Generates a random password of a given length

    Attributes:
        length (int): Length of the password to generate. Default is 12."""
    allowed_chars = [string.ascii_uppercase, "!@#$%^*()_+"]
    password = [secrets.choice(allowed_chars[0]) for n in range(length//4)]
    password += [secrets.choice(allowed_chars[1]) for n in range(length//4)]
    length = length - 2 * (length // 4)
    allowed_chars = [string.ascii_lowercase,
                     string.digits,
                     "-=;,./"]
    password += [secrets.choice(allowed_chars[0]) for n in range(length//2)]
    length = length - (length // 2)
    password += [secrets.choice(allowed_chars[1]) for n in range(length//2)]
    length = length - (length // 2)
    password += [secrets.choice(allowed_chars[2]) for n in range(length)]
    password = ''.join(password)
    return password


def test_generate_password():
    """Runs 100 tests to generate passwords and verify that each of
    the generated passwords meets all the criteria."""
    for _ in range(100):
        password = generate_password(12)
        error = f"ERROR: generated password -- {password} --"
        assert len(password) >= 12, \
            f"{error} length is less 12."
        assert any(c.isupper() for c in password), \
            f"{error} did not contain at least one uppercase letter."
        assert any(c.islower() for c in password), \
            f"{error} did not contain at least one lowercase letter."
        assert any(c.isdigit() for c in password), \
            f"{error} did not contain at least one digit."
        assert any(c in "!@#$%^*()_+" for c in password), \
            f"{error} did not contain at least one special character."
        print(f"Generated password: {password}")


if __name__ == "__main__":
    test_generate_password()
