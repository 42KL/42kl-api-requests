# create_users.py
"""Creates external users on the intranet for Discovery Piscine
"""

import json
import re
import sys
from time import sleep
from FtApi import FtApi
from FtCSV import read_csv_into_list
from FtUser import FtUser
from FtUtils import ft_write_error, ft_write_info, ft_write_success


def create_user(ft_user: FtUser = None, ft_api: FtApi = None):
    """Creates a user on the intranet"""
    assert ft_user is not None and isinstance(ft_user, FtUser), \
        "Invalid FtUser object."
    assert ft_user.is_postable, ft_user.whats_wrong()
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    ft_write_info(f"POST to {ft_api.site}/v2/users")
    try:
        response = ft_api.oauth.post(f"{ft_api.site}/v2/users",
                                     json=ft_user.user)
        if int(response.status_code) != 201:
            raise Exception("Failed: User creation failure")
    except BaseException as error:
        raise error
        return error
    response = json.loads(response.text)
    message = f"User created for {ft_user.user['user']['email']}:"
    message += response["login"]
    ft_write_success(message)
    return response


def add_user_to_cursus(ft_user: FtUser = None, ft_api: FtApi = None):
    """Adds a user to cursus_users."""
    assert ft_user is not None and isinstance(ft_user, FtUser), \
        "Invalid FtUser object."
    if ft_api is None or not isinstance(ft_api, FtApi):
        ft_api = FtApi()
    ft_write_info(f"POST to {ft_api.site}/v2/cursus_users")
    if "user_id" not in ft_user.cursus["cursus_user"] or \
            ft_user.cursus["cursus_user"]["user_id"] is None:
        ft_user.cursus["cursus_user"]["user_id"] = ft_user.user["user"]["id"]
    try:
        response = ft_api.oauth.post(f"{ft_api.site}/v2/cursus_users",
                                     json=ft_user.cursus)
        if int(response.status_code) != 201:
            raise Exception("Failed: Cursus enrollment failure")
    except BaseException as error:
        raise error
        return error
    message = ft_user.user["user"]["login"] + " enrolled to "
    message += ft_user.cursus["cursus_user"]["cursus_id"]
    ft_write_success(message)
    return json.loads(response.text)


def main():
    """Creates external users on the intranet for Discovery Piscine
    """
    if len(sys.argv) == 2:
        CSV_FILE = sys.argv[1]
    else:
        CSV_FILE = "test.csv"
    POOL_YEAR = "2025"
    POOL_MONTH = "june"
    BEGIN_AT = "2025-06-23T00:00:42.000Z"
    END_AT = "2025-06-25T15:59:42.000Z"
    CURSUS_ID = "79"  # This is Discovery AI

    try:
        csv_data = read_csv_into_list(CSV_FILE)
        for row in csv_data:
            first_name = row[0]
            last_name = row[1]
            usual_first_name = row[2]
            email = row[3]
            res = row.copy()
            if not re.search("^[^@]+@[^@.]+.[^@]+$", email):
                res.append("login")
                print(",".join(res))
                continue
            ft_api = FtApi()
            ft_user = FtUser(email=email,
                             first_name=first_name,
                             last_name=last_name,
                             usual_first_name=usual_first_name,
                             campus_id=ft_api.campus,
                             pool_year=POOL_YEAR,
                             pool_month=POOL_MONTH,
                             cursus_id=CURSUS_ID,
                             begin_at=BEGIN_AT,
                             end_at=END_AT)
            api_status = create_user(ft_user, ft_api)
            if isinstance(api_status, str):
                res.append(api_status)
                continue
            res.append(api_status["login"])
            ft_user.user["user"]["login"] = api_status["login"]
            ft_user.user["user"]["id"] = api_status["id"]
            sleep(0.6)
            api_status = add_user_to_cursus(ft_user, ft_api)
            if isinstance(api_status, str):
                res.append(api_status)
            print(",".join(res))
            sleep(0.6)
    except BaseException as error:
        ft_write_error(f"Error: {error}")
        return
    return


if __name__ == "__main__":
    main()
