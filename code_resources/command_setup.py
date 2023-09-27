from discord import Interaction, TextChannel
from .utility.cat_run_task import CatLoop
from .utility.util import db, tevcnoio


async def setup_cb(interaction: Interaction, setup_tasks: dict[int, CatLoop]):
    if interaction.guild is not None and isinstance(interaction.channel, TextChannel):
        cid = interaction.channel.id
        gid = interaction.guild.id
        print(gid, cid)
        setup_tasks[cid] = CatLoop(interaction.channel, interaction.guild, 0)
        await setup_tasks[cid].start()
        guild_cscwg_db: dict[int, list[int]] = tevcnoio(
            db["cscwg"].get(gid), gid, {}, db["cscwg"]
        )
        print("db, guild db:", db, guild_cscwg_db)
        channel_cscwg_db: list[int] = tevcnoio(
            guild_cscwg_db.get(cid), cid, [], guild_cscwg_db
        )
        print("guild db after creation:", guild_cscwg_db)
        print("channel db:", channel_cscwg_db)
        channel_cscwg_db.append(cid)
        print("guild db after set:", guild_cscwg_db)
        db["cscwg"].update(guild_cscwg_db)
        print("after set update:", db, db["cscwg"])
        db.save("cscwg")
        await interaction.send(
            f"oki! i will now send cats in #{interaction.channel.name}!"
        )
    else:
        await interaction.send("skull emoji :skull:")
