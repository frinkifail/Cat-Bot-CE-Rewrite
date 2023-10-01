from discord import Interaction, TextChannel
from .utility.cat_run_task import CatLoop
from .utility.util import db, tevcnoio


async def setup_cb(interaction: Interaction, setup_tasks: dict[int, CatLoop]):
    if interaction.guild is not None and isinstance(interaction.channel, TextChannel):
        message = await interaction.send("ok setting up")
        cid = interaction.channel.id
        gid = interaction.guild.id
        # print(gid, cid)
        setup_tasks[cid] = CatLoop(interaction.channel, interaction.guild, 0)
        success = await setup_tasks[cid].start()
        if not success:
            await interaction.send("this channel is already setup")
            return
        # guild_cscwg_db: dict[int, list[int]] = tevcnoio(
        #     db["cscwg"].get(gid), gid, {}, db["cscwg"]
        # )
        # channel_cscwg_db: list[int] = tevcnoio(
        #     guild_cscwg_db.get(cid), cid, [], guild_cscwg_db
        # )
        # channel_cscwg_db.append(cid)
        # db["cscwg"].update(guild_cscwg_db)
        # db.save("cscwg")
        if db["cscwg"].get(gid) is None:
            db["cscwg"][gid] = []
        db["cscwg"][gid].append(cid)
        db.save("cscwg")
        await message.edit(f"oki! i will now send cats in #{interaction.channel.name}!")
    else:
        await interaction.send("skull emoji :skull:")
