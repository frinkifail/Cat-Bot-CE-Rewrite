from discord import Interaction, TextChannel

from .utility.cat_run_task import CatLoop
from .utility.util import db


async def forget_cb(interaction: Interaction, setup_tasks: dict[int, CatLoop]):
    if interaction.guild is None or not isinstance(interaction.channel, TextChannel):
        await interaction.send("what ur tryna do??")
        return
    cid = interaction.channel.id
    gid = interaction.guild.id
    try:
        db.reload("cscwg")
        setup_tasks[cid].running = False
        # print(db['cscwg'])
        db["cscwg"][str(gid)].remove(cid)
        db.save("cscwg")
        await interaction.send(
            f"share if you have dementia (successfully forgort this channel)"
        )
    except KeyError or ValueError:
        await interaction.send(f"{interaction.channel} isn't setup yet")
