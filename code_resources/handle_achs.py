from discord import Member, Message, TextChannel, User

from .achivements import Achivement, AchivementManager, UnlockedUsing
from .utility.util import db
from .current_achs import achivements


async def handle_ach(message: Message, msg: str, user: User | Member):
    async def unlock_ach(ach_name: str, ach_type: UnlockedUsing, ach_desc: str):
        # print("ADB:", adb)
        ach = adb.get(ach_name)
        # print("ACH:", ach)
        if ach is not None:
            success = AchivementManager.unlock(ach, str(user))
        else:
            adb[ach_name] = AchivementManager.new(ach_type, description=ach_desc)
            success = AchivementManager.unlock(adb[ach_name], str(user))
        if isinstance(message.channel, TextChannel):
            if success:
                await message.channel.send(
                    f"{user.global_name} just unlocked {ach_name}!"
                )
            else:
                if user.dm_channel is not None:
                    await user.dm_channel.send(f"you already unlocked {ach_name}")
                else:
                    await message.reply(
                        f"you already unlocked {ach_name}"
                    )  # haha out for everyone to see!!
                    # and yes, i do know how to use `User|Member#create_dm`, I'm just too lazy.
        else:
            print("oh, interaction.channel isn't a textchannel...\nthat's a shame.")
        db["achs"].update({str(user.id): adb})
        db.save("achs")

    adb: dict[str, Achivement] = db.uget(user.id, "achs")
    for k, v in achivements.items():
        if v["unlocked_using"] == "exact":
            if v["phrase"] == msg:
                await unlock_ach(k, "exact", v["description"])
        if v["unlocked_using"] == "includes":
            if v["phrase"] in msg:
                await unlock_ach(k, "includes", v["description"])
