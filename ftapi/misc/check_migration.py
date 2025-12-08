# check_migration.py
"""
Checks if Cursus Migration (8 December 2025) is done for all eligible Cadets
"""


from time import sleep
from FtCursus import get_cursus_users
from FtUtils import ft_write_error
from get_user_quests import get_user_quests_by_id


def check_migration():
    """
    Checks cursus migration status for eligible cadets.

    Synopsis:
    1. GET eligible cadets (begin_at between 2025-09-15 to 2025-12-08).
    2. GET quests for each Cadet from user_id.
    3. PRINT 1/0 if quests include 42next (id=`128`; slug=`42next`).
    """
    try:
        CURSUS_ID="21"
        BEGIN_DATE="2025-09-15"
        END_DATE="2025-12-08"
        cursus_users = get_cursus_users(ft_api=None, cursus_id=CURSUS_ID,
                                        begin_date=BEGIN_DATE,
                                        end_date=END_DATE)
        assert len(cursus_users) > 0, "No cursus users found."
        sleep(0.8)
        print("Login,Migrated")
        for cursus_user in cursus_users:
            user_id = f"{cursus_user['user']['id']}"
            login = cursus_user["user"]["login"]
            quests = get_user_quests_by_id(ft_api=None, user_id=user_id)
            quests = [ quest["id"] for quest in quests ]
            if 37 in quests and 128 in quests:
                print(f"{login},1")
            else:
                print(f"{login},0")
            sleep(0.8)
    except BaseException as error:
        raise error
        return
    return


if __name__ == "__main__":
    try:
        check_migration()
    except BaseException as error:
        ft_write_error(error)
        exit()
