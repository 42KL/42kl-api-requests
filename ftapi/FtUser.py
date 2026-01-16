# FtUser.py
"""The FtUser class/object"""


from dataclasses import dataclass, asdict
from datetime import datetime as dt


@dataclass
class FtCursusUser:
    """The FtCursusUser dataclass: to store data and methods for
    creating a cursus user for a given user using 42 API (v2).
    Methods include:
    - asdict(): returns defined attributes as a dictionary.
    """
    user_id: str = None
    cursus_id: str = None
    begin_at: str = None
    end_at: str = None

    def asdict(cls):
        """Returns all non-None attributes as a dictionary"""
        cls_dict = asdict(cls)
        cls_dict = {k: cls_dict[k] for k in cls_dict.keys()
                    if cls_dict[k] is not None}
        return cls_dict


@dataclass
class FtUser:
    """The FtUser dataclass: to store data and methods for
    creating a user using the 42 API (v2).
    Methods include:
    - asdict(): returns defined attributes as a dictionary.
    - is_postable(): validates if data is safe to POST (any missing values).
    - whats_wrong(): returns list of undefined keys as a string (error msg).
    """
    REQUIRED = ["email", "first_name", "last_name", "kind",
                "campus_id", "pool_year", "pool_month"]
    email: str = None
    first_name: str = None
    last_name: str = None
    usual_first_name: str = None
    password: str = None
    kind: str = "external"
    campus_id: str = None
    skip_welcome_mail: str = "true"
    pool_year: str = dt.now().year
    pool_month: str = dt.now().strftime("%B").lower()

    def asdict(cls):
        """Returns all non-None attributes as a dictionary"""
        cls_dict = asdict(cls)
        cls_dict = {key: cls_dict[key] for key in cls_dict.keys()
                    if cls_dict[key] is not None}
        return cls_dict

    def is_postable(cls):
        """Checks if REQUIRED keys are defined"""
        for key in cls.REQUIRED:
            if key not in cls.asdict().keys():
                return False
        return True

    def whats_wrong(cls):
        """Return as a string list of REQUIRED keys that are not defined"""
        undef_keys = [key for key in cls.REQUIRED 
                       if key not in cls.asdict().keys()]
        if len(undef_keys) == 0:
            return
        return f"Missing values: {', '.join(undef_keys)}"
