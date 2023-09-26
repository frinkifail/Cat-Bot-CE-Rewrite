from discord import Member, Message, TextChannel, User

from .achivements import Achivement, UnlockedUsing
from .utility.util import tevcnoio, db
from .current_achs import achivements


async def handle_ach(message: Message, msg: str, user: User | Member):
    async def unlock_ach(ach_name: str, ach_type: UnlockedUsing):
        ach = adb.get(ach_name)
        if ach is not None:
            ach.unlock(user)
        else:
            adb[ach_name] = Achivement(ach_type)
            adb[ach_name].unlock(user)
        if isinstance(message.channel, TextChannel):
            await message.channel.send(f"{user.display_name} just unlocked {ach_name}!")
        else:
            print("oh, interaction.channel isn't a textchannel...\nthat's a shame.")

    a = user.id
    adb: dict[str, Achivement] = tevcnoio(db["achs"].get(str(a)), str(a), {}, db)
    for k, v in achivements.items():
        if v.unlocked_using == "exact":
            if v.phrase == msg:
                await unlock_ach(k, "exact")
        if v.unlocked_using == "includes":
            if msg in v.phrase:
                await unlock_ach(k, "includes")
