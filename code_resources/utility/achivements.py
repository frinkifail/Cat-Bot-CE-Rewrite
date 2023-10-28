from typing import Literal, TypeAlias, TypedDict, TYPE_CHECKING
from .util import db

from nextcord import User, Message, Member
from nextcord import TextChannel

UnlockedUsing: TypeAlias = Literal["exact", "includes", "external"]


class Achivement(TypedDict):
    unlocked: bool
    unlocked_by: str | None
    unlocked_using: UnlockedUsing
    phrase: str
    description: str
    hidden: bool
    id: str | None


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
    async def unlock_send(
        message: Message,
        adb: dict[str, Achivement],
        user: User | Member,
        ach_name: str,
    ):
        from .current_achs import achivements

        ach = adb.get(ach_name)
        if ach is not None:
            success = AchivementManager.unlock(ach, str(user))
        else:
            # adb[ach_name] = AchivementManager.new(None, ach_type, description=ach_desc)
            temp_ach = achivements.get(ach_name)
            if temp_ach is None:
                # temp_2_ach =
                for v in achivements.values():
                    if v["id"] == ach_name:
                        adb[ach_name] = v
            else:
                adb[ach_name] = temp_ach

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

    @staticmethod
    def new(
        id: str | None,
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
            "id": id,
        }
