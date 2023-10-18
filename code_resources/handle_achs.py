from discord import Member, Message, TextChannel, User

from .achivements import Achivement, AchivementManager, UnlockedUsing
from .utility.util import db
from .current_achs import achivements


async def handle_ach(message: Message, msg: str, user: User | Member):
    adb: dict[str, Achivement] = db.uget(user.id, "achs")
    for k, v in achivements.items():
        # Could've used match but whatever
        if v["unlocked_using"] == "exact":
            if v["phrase"] == msg:
                await AchivementManager.unlock_send(message, adb, user, k)
        if v["unlocked_using"] == "includes":
            if v["phrase"] in msg:
                await AchivementManager.unlock_send(message, adb, user, k)
