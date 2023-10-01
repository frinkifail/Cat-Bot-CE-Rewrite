from typing import Literal, TypeAlias, TypedDict

UnlockedUsing: TypeAlias = Literal["exact", "includes"]


class Achivement(TypedDict):
    unlocked: bool
    unlocked_by: str | None
    unlocked_using: UnlockedUsing
    phrase: str
    description: str
    hidden: bool


class AchivementManager:
    @staticmethod
    def unlock(achivement: Achivement, by: str):
        # print("Unlocked:", achivement["unlocked"])
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
        description: str = "<unset>",
        hidden: bool = False,
    ) -> Achivement:
        return {
            "phrase": phrase,
            "unlocked": unlocked,
            "unlocked_by": unlocked_by,
            "unlocked_using": unlocked_using,
            "description": description,
            "hidden": hidden,
        }
