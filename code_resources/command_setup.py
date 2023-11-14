from discord import Interaction, TextChannel
from .utility.cat_run_task import CatLoop
from .utility.util import db


async def setup_cb(interaction: Interaction, setup_tasks: dict[int, CatLoop]):
    if (
        interaction.guild is None
        or not isinstance(interaction.channel, TextChannel)
        or not interaction.user.guild_permissions.administrator  # type: ignore
    ):
        await interaction.send("skull emoji :skull:")
        return
    message = await interaction.send("ok setting up")
    cid = interaction.channel.id
    gid = interaction.guild.id
    # print(gid, cid)
    if setup_tasks.get(cid) is not None:
        setup_tasks[cid] = CatLoop(interaction.channel, interaction.guild, 0)
        success = await setup_tasks[cid].start()
        await setup_tasks[cid].spawn()  # incase something goes wrong or smth
        if not success:
            await interaction.send("what how")
            return
    if db["cscwg"].get(gid) is None:
        db["cscwg"][gid] = []
    if cid in db["cscwg"][gid]:
        await message.edit(f"you dumb this channel is already setup")
        return
    db["cscwg"][gid].append(cid)
    db.save("cscwg")
    await message.edit(f"oki! i will now send cats in #{interaction.channel.name}!")
