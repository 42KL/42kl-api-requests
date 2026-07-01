# FtExam.py
"""The exam class for storing exam data.
Mainly used as json payload for API calls."""

from dataclasses import dataclass, asdict


@dataclass
class FtExam:
    """The FtExam dataclass: to store data and methods for
    creating an exam using 42 API (v2).

    Methods include:
    - asdict(): returns defined attributes as a dictionary.
    """
    name: str = None
    begin_at: str = None
    end_at: str = None
    location: str = None
    ip_range: str = None
    visible: bool = True
    max_people: int = None
    campus_id: int = None
    activate_waitlist: bool = False
    project_ids: list = None

    def asdict(cls):
        """Returns all defined (not None) attributes as a dictionary"""
        cls_dict = asdict(cls)
        cls_dict = {k: cls_dict[k] for k in cls_dict.keys()
                    if cls_dict[k] is not None}
        return cls_dict
