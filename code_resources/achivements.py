from typing import Literal, TypeAlias
from discord import Member, User

UnlockedUsing: TypeAlias = Literal["exact", "includes"]


class Achivement:
    def __init__(self, using: UnlockedUsing, phrase: str = "") -> None:
        self.unlocked: bool = False
        self.unlocked_by: User | Member | None = None
        self.unlocked_using = using
        self.phrase = phrase

    def unlock(self, by: User | Member):
        if not self.unlocked:
            self.unlocked = True
            self.unlocked_by = by
            return True
        else:
            return False
