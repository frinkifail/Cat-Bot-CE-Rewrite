from time import time
from discord import Message
from nextcord.utils import get
from .utility.achivements import AchivementManager

from .utility.cat_run_task import CatLoop
from .utility.util import tevcnoio, db


async def catch_cb(
    message: Message,
    gid: int,
    cid: int,
    adb: dict[str, int],
    setup_tasks: dict[int, CatLoop],
    a: int,
):
    if gid == 0 or message.guild is None:
        await message.reply("sureeeeee")
        return
    # ctype_guild = tevcnoio(str(gid), {}, db["cattype"])
    # ctype: str = tevcnoio(str(cid), "none", ctype_guild)
    if db["cattype"].get(str(gid)) is None:
        db["cattype"][str(gid)] = {}
    if db["cattype"][str(gid)].get(str(cid)) is None:
        ctype = "none"
    else:
        ctype = db["cattype"][str(gid)][str(cid)]
    if ctype == "none":
        await message.reply("har har har you said cat")
    else:
        db.reload("times")
        tevcnoio(ctype, 0, adb)
        adb[ctype] += 1
        # print(adb)
        db["cats"].update({a: adb})
        db.save("cats")
        await message.delete()
        cmsg = setup_tasks[cid].current_msg
        if cmsg is not None:
            await cmsg.delete()
            setup_tasks[cid].cat_active = False
        emoji = get(message.guild.emojis, name=ctype + "cat")
        dn = message.author.global_name
        # print("Display name:", dn)
        if dn == "@everyone" or dn == "@here":
            dn = "YouTried"
        timing: float | str = round(
            time() - db["times"].get(str(gid), {}).get(str(cid), 2147483647), 2
        )
        if isinstance(timing, float) and timing < 0:
            timing = "undefined"
        if timing == 3.14:
            await AchivementManager.unlock_send(
                message, db.uget(a, "achs"), message.author, "pi catch"
            )
        await message.channel.send(
            f" \
{dn} cought {emoji} {ctype.capitalize()} cat!!!!1!\n\
You now have {adb[ctype]} cats of dat type!!!\n\
this fella was cought in {timing} seconds!!!!"
        )
        db["cattype"][str(gid)][str(cid)] = "none"
        db["cat active"][str(gid)][str(cid)] = False
        db.save("cat active")
