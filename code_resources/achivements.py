from typing import Literal, TypeAlias, TypedDict
from discord import Member, User

UnlockedUsing: TypeAlias = Literal["exact", "includes"]


# class Achivement:
#     def __init__(self, using: UnlockedUsing, phrase: str = "") -> None:
#         self.unlocked: bool = False
#         self.unlocked_by: User | Member | None = None
#         self.unlocked_using = using
#         self.phrase = phrase

#     def unlock(self, by: User | Member):
#         # print("unlocked before set:", self.unlocked)
#


class Achivement(TypedDict):
    unlocked: bool
    unlocked_by: str | None
    unlocked_using: UnlockedUsing
    phrase: str


class AchivementManager:
    @staticmethod
    def unlock(achivement: Achivement, by: str):
        print("Unlocked:", achivement["unlocked"])
        if not achivement["unlocked"]:
            achivement["unlocked"] = True
            achivement["unlocked_by"] = by
            return True
        else:
            return False

    @staticmethod
    def new(
        unlocked_using: UnlockedUsing,
        unlocked: bool = False,
        unlocked_by: str | None = None,
        phrase: str = "",
    ) -> Achivement:
        return {
            "phrase": phrase,
            "unlocked": unlocked,
            "unlocked_by": unlocked_by,
            "unlocked_using": unlocked_using,
        }
