# create_users.py
"""Creates external users on the intranet for Discovery Piscine
"""

import json
import re
import secrets
import string
import sys
from time import sleep
from FtApi import FtApi
from FtCSV import read_csv_into_list
from FtCursus import compute_cursus_end_from_begin
from FtDateTime import is_valid_date
from FtUser import FtUser, FtCursusUser
from FtUtils import ft_write_error, ft_write_info, ft_write_success


def generate_password(length: int = 12) -> str:
    """Generates a random password of a given length

    Attributes:
        length (int): Length of the password to generate. Default is 12."""
    allowed_chars = [string.ascii_lowercase,
                     string.ascii_uppercase,
                     string.digits,
                     "!@#$%^*()-_=+[]{};:|,./?"]
    password = [secrets.choice(allowed_chars[n % 4]) for n in range(length)]
    password = ''.join(password)
    return password


def create_user(ft_user: FtUser = None, ft_api: FtApi = None):
    """Creates a user on the intranet"""
    assert ft_user is not None and isinstance(ft_user, FtUser), \
        "Invalid FtUser object."
    assert ft_user.is_postable(), ft_user.whats_wrong()
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    ft_write_info(f"POST to {ft_api.site}/v2/users")
    try:
        user_dict = {"user": ft_user.asdict()}
        response = ft_api.oauth.post(f"{ft_api.site}/v2/users", json=user_dict)
        if int(response.status_code) != 201:
            error = "ERROR: User creation failure."
            error += f"\n{response.status_code}: {response.text}."
            raise Exception(error)
        response.raise_for_status()
        response_text = json.loads(response.text)
        response.close()
    except BaseException:
        raise
    message = f"User created for {ft_user.email}:"
    message += response_text["login"]
    ft_write_success(message)
    return response_text


def add_user_id_to_cursus(ft_api: FtApi = None,
                          user_id: str = None,
                          cursus_id: str = None,
                          begin_date: str = None) -> dict:
    """Create a cursus user using 42 API (v2)"""
    assert user_id is not None and isinstance(user_id, str) and \
        len(user_id) > 0, "Undefined/invalid user_id, doing nothing."
    assert cursus_id is not None and isinstance(cursus_id, str) and \
        len(cursus_id) > 0, "Undefined/invalid cursus_id, doing nothing."
    assert begin_date is not None and isinstance(begin_date, str) and \
        len(begin_date) > 0 and is_valid_date(begin_date), \
        "Undefined/invalid begin_date, doing nothing."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    BEGIN_AT = f"{begin_date} 00:00:42"
    END_AT = compute_cursus_end_from_begin(cursus_id=cursus_id,
                                           begin_date=begin_date)
    cursus_user = FtCursusUser(user_id=user_id, cursus_id=cursus_id,
                               begin_at=BEGIN_AT, end_at=END_AT)
    cursus_user = {"cursus_user": cursus_user.asdict()}
    post_url = f"{ft_api.site}/v2/cursus_users"
    post_re = ft_api.oauth.post(post_url, json=cursus_user)
    post_re.raise_for_status()
    return post_re


def main():
    """Creates external users on the intranet for Discovery Piscine
    """
    USAGE = f"Usage: python3 {sys.argv[0]} users.csv CURSUS_ID BEGIN_DATE"
    SUPPORTED_CURSUS = ["79", "80"]
    try:
        assert len(sys.argv) == 4, USAGE
        CSV_FILE = sys.argv[1]
        CURSUS_ID = sys.argv[2]
        assert CURSUS_ID in SUPPORTED_CURSUS, \
            f"\"{CURSUS_ID}\" not supported.\n{USAGE}"
        BEGIN_DATE = sys.argv[3]
        assert is_valid_date(BEGIN_DATE), \
            f"\"{BEGIN_DATE}\" not a valid date.\n{USAGE}"
        csv_data = read_csv_into_list(CSV_FILE)
        ft_api = FtApi()
        for row in csv_data:
            first_name = row[0]
            last_name = row[1]
            usual_first_name = row[2]
            email = row[3]
            res = row.copy()
            if not re.search("^[^@]+@[^@.]+.[^@]+$", email):
                res.append("login")
                res.append("password")
                print(",".join(res))
                continue
            ft_user = FtUser(email=email,
                             first_name=first_name,
                             last_name=last_name,
                             usual_first_name=usual_first_name,
                             password=generate_password(),
                             campus_id=ft_api.campus)
            api_status = create_user(ft_user, ft_api)
            if isinstance(api_status, Exception):
                res.append(str(api_status))
                print(",".join(res))
                ft_api = None
                del ft_api
                continue
            res.append(api_status["login"])
            res.append(ft_user.password)
            sleep(0.6)
            post_re = add_user_id_to_cursus(ft_api=ft_api,
                                            user_id=str(api_status["id"]),
                                            cursus_id=CURSUS_ID,
                                            begin_date=BEGIN_DATE)
            if int(post_re.status_code) != 201:
                error = "ERROR: Failed to add user to cursus."
                error += f"\n{post_re.status_code}: {post_re.text}."
                res.append(error)
                print(",".join(res))
                ft_api = None
                del ft_api
                raise Exception(error)
            post_re.close()
            print(",".join(res))
            sleep(0.6)
    except BaseException as error:
        ft_write_error(f"Error: {error}")
        return
    return


if __name__ == "__main__":
    main()
