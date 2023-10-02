from time import time
from typing import Any
from discord import Message
from nextcord.utils import get

from code_resources.utility.cat_run_task import CatLoop
from .utility.util import tevcnoio, db


async def catch_cb(
    message: Message,
    gid: int,
    cid: int,
    adb: dict[str, Any],
    setup_tasks: dict[int, CatLoop],
    a: int,
):
    if gid == 0 or message.guild is None:
        await message.reply("sureeeeee")
        return
    ctype_guild = tevcnoio(db["cattype"].get(str(gid)), str(gid), {}, db["cattype"])
    ctype: str = tevcnoio(ctype_guild.get(str(cid)), str(cid), "none", ctype_guild)
    if ctype == "none":
        await message.reply("har har har you said cat")
    else:
        db.reload("times")
        tevcnoio(adb.get(ctype), ctype, 0, adb)
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
        timing: float = time() - db["times"].get(str(gid), {}).get(str(cid), 2147483647)
        if timing < 0:
            timing = -1
        await message.channel.send(
            f" \
{dn} cought {emoji} {ctype.capitalize()} cat!!!!1!\n\
You now have {adb[ctype]} cats of dat type!!!\n\
this fella was cought in {timing} seconds!!!!"
        )
        db["cattype"][str(gid)][str(cid)] = "none"
