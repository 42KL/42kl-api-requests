# FtAchievementUser.py
"""Data class for storing achievement user data."""

from dataclasses import dataclass, asdict


@dataclass
class FtAchievementUser:
    """The FtAchievementUser dataclass: to store data and methods for
    creating an achievement user for a given user using 42 API (v2).
    Methods include:
    - asdict(): returns defined attributes as a dictionary.
    """
    user_id: int = None
    achievement_id: int = None
    nbr_of_success: int = None
    rewarded: bool = False

    def asdict(cls):
        """Returns only non-None attributes as a dictionary"""
        cls_dict = asdict(cls)
        cls_dict = {k: cls_dict[k] for k in cls_dict.keys()
                    if cls_dict[k] is not None}
        return cls_dict


def test():
    """Test FtAchievementUser dataclass"""
    user_id = 12345
    achievement_id = 67890
    nbr_of_success = 1
    rewarded = True
    achievement_user = FtAchievementUser(
        user_id=user_id,
        achievement_id=achievement_id,
        nbr_of_success=nbr_of_success,
        rewarded=rewarded
    )
    print(achievement_user)
    print(achievement_user.asdict())
    achievement_user = FtAchievementUser(
        achievement_id=achievement_id,
        nbr_of_success=nbr_of_success,
        rewarded=rewarded
    )
    print(achievement_user)
    print(achievement_user.asdict())
    achievement_user = FtAchievementUser(
        user_id=user_id,
        nbr_of_success=nbr_of_success,
        rewarded=rewarded
    )
    print(achievement_user)
    print(achievement_user.asdict())
    achievement_user = FtAchievementUser(
        user_id=user_id,
        achievement_id=achievement_id,
        rewarded=rewarded
    )
    print(achievement_user)
    print(achievement_user.asdict())
    achievement_user = FtAchievementUser(
        user_id=user_id,
        achievement_id=achievement_id,
        nbr_of_success=nbr_of_success
    )
    print(achievement_user)
    print(achievement_user.asdict())


if __name__ == "__main__":
    test()
