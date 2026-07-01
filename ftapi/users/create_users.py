# create_users.py
"""Creates external users on the intranet for Discovery Piscine
"""

import json
import re
import sys
from time import sleep
from FtApi import FtApi
from FtUser import FtUser
from users.add_user_to_cursus import add_user_id_to_cursus
from utils.ft_datetime import is_valid_date
from utils.io.ft_read_csv import read_csv_into_list
from utils.io.ft_handle_error import ft_handle_error
from utils.io.ft_write_stderr import ft_write_info, \
                                     ft_write_success
from utils.generate_password import generate_password


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
        ft_handle_error(error)  # will exit(1)
        return
    return


if __name__ == "__main__":
    main()
