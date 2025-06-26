# FtUser.py
"""The FtUser class/object"""


class FtUser:
    """The FtUser class/object contains
    - dictionary to contain data for a user to create on 42 intranet.
    - method to validate if dictionary is valid (no missing required value.
    """

    def __init__(cls, email=None, first_name=None, last_name=None,
                 usual_first_name=None, campus_id=None,
                 pool_year=None, pool_month=None,
                 cursus_id=None, begin_at=None, end_at=None):
        """on initialisation, dictionary is created.
        """
        cls.required = ["email", "first_name", "last_name", "kind",
                        "campus_id", "pool_year", "pool_month"]
        cls.user = dict(
                user=dict(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        kind="external",
                        campus_id=campus_id,
                        skip_welcome_mail="true",
                        pool_year=pool_year,
                        pool_month=pool_month
                        )
                )
        if usual_first_name is not None and usual_first_name != "":
            cls.user["user"]["usual_first_name"] = usual_first_name
        cls.cursus = dict(
                cursus_user=dict(
                        cursus_id=cursus_id,
                        begin_at=begin_at
                )
        )
        if end_at is not None and end_at != "":
            cls.cursus["cursus_user"]["end_at"] = end_at

    def __str__(cls):
        """returns the values in the dictionary
        """
        return str(cls.user)

    def __repr__(cls):
        """returns the values in the dictionary
        """
        return repr(cls.user)

    def is_postable(cls):
        """returns if all required parameters are not None
        """
        state = cls.user["user"]
        for key in cls.required:
            if state[key] is None:
                return False
        return True

    def whats_wrong(cls):
        """prints information on what"s wrong (which required values not set)
        """
        is_missing = "is required but not set"
        state = cls.user["user"]
        for key in cls.required:
            if state[key] is None:
                return f"{key} {is_missing}."
        return
