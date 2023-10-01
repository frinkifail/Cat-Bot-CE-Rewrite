from typing import Any
from discord import Color, Embed, Interaction, User
from nextcord.ext.commands import Bot
from nextcord.utils import get
from .utility.util import EMOJI_GUILD_ID, db


async def inventory_cb(interaction: Interaction, person: User | None, bot: Bot):
    msg = await interaction.send("workin on it!")
    viewing_self = False
    if person is not None:
        user = person
    elif interaction.user is not None:
        user = interaction.user
    else:
        await interaction.send("something went wrong")
        return
    db.reload("cats")
    adb: dict[str, Any] = db.uget(user.id, "cats")
    embed = Embed(
        color=Color.blurple(),
        title=f"{'Your' if viewing_self else user.global_name}'s cats",
    )
    for k, v in adb.items():
        guild = await bot.fetch_guild(EMOJI_GUILD_ID)
        emoji = get(guild.emojis, name=f"{k}cat")
        embed.add_field(
            name=f"{f'{emoji} ' if emoji else '(no emoji found kek) '}{k.capitalize()}",
            value=v,
        )
    if embed.fields.__len__() == 0:
        embed.add_field(name="no cats", value="go catch some")
    await msg.edit("", embed=embed)
