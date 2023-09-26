#!/Users/waadna/.pyenv/shims/python
from os import execv
from sys import argv, executable
from typing import Any, Optional
import nextcord as nc
from nextcord.ext import commands
from code_resources.handle_achs import handle_ach
from code_resources.utility.cat_run_task import CatLoop

# from code_resources.! unused ! command_say

# from code_resources.utility.util import (
#     init_data,
#     load_json,
#     read_file,
#     try_get,
#     update_json,
# )
from code_resources.utility.util import (
    EMOJI_GUILD_ID,
    db,
    init_data,
    read_file,
    tevcnoio,
)

init_data()

bot = commands.Bot(intents=nc.Intents.all())
# print(db["cats"])

setup_tasks: dict[int, CatLoop] = {}  # ChannelID: Loop
cscwg: dict[
    int, list[int]
] = {}  # Current Setup Channels With Guild # {GuildID: [ChannelID, ...]}


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user.display_name}")
        await bot.change_presence(
            activity=nc.Activity(type=nc.ActivityType.playing, name="with Cat Bot"),
            status=nc.Status.dnd,
        )
        catbot_channel = await bot.fetch_channel(1151851013637152859)
        if isinstance(catbot_channel, nc.TextChannel):
            await catbot_channel.send("oki i restarted")
        if setup_tasks.__len__() == 0:
            # for i in db
            # TODO: setup for everything in db[cscwg]
            for k, v in db["cscwg"].items():
                k: int  # Explicit typing
                v: list[int]
                guild = await bot.fetch_guild(k)
                channels: list[nc.guild.GuildChannel | nc.Thread] = []
                for i in v:
                    channel = await guild.fetch_channel(i)
                    channels.append(channel)
                for i in channels:
                    if isinstance(i, nc.TextChannel):
                        setup_tasks[i.id] = CatLoop(i, guild, 0)
                        await setup_tasks[i.id].start()
    else:
        print("Not logged in (how?)")


@bot.slash_command("setup", "setup the bot")
async def setup(interaction: nc.Interaction):
    if interaction.guild is not None and isinstance(
        interaction.channel, nc.TextChannel
    ):
        cid = interaction.channel.id
        gid = interaction.guild.id
        print(gid, cid)
        setup_tasks[cid] = CatLoop(interaction.channel, interaction.guild, 0)
        await setup_tasks[cid].start()
        # db['cscwg'].update({gid: [cid]})
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


@bot.slash_command("inventory", "see your or other's inventory")
async def inventory(interaction: nc.Interaction, person: Optional[nc.User]):
    viewing_self = False
    if person is not None:
        user = person
    elif interaction.user is not None:
        user = interaction.user
    else:
        await interaction.send("something went wrong")
        return
    a = user.id
    # print(db['cats'], a, db['cats'].get(a))
    adb: dict[str, Any] = tevcnoio(db["cats"].get(str(a)), str(a), {}, db)
    embed = nc.Embed(
        color=nc.Color.blurple(),
        title=f"{'Your' if viewing_self else user.display_name}'s cats",
    )
    # embed.add_field()
    for k, v in adb.items():
        guild = await bot.fetch_guild(EMOJI_GUILD_ID)
        emoji = nc.utils.get(guild.emojis, name=f"{k}cat")
        embed.add_field(
            name=f"{f'{emoji} ' if emoji else '(no emoji found kek) '}{k.capitalize()}",
            value=v,
        )
    if embed.fields.__len__() == 0:
        embed.add_field(name="no cats", value="go catch some")
    await interaction.send(embed=embed)


@bot.event
async def on_message(message: nc.Message):
    # print("on message")
    # print(message)
    c = message.content
    a = message.author.id
    gid = (
        message.guild.id if message.guild else 0
    )  # smhhhh null checks for example they send in dms or smthhhh
    cid = message.channel.id
    adb: dict[str, Any] = tevcnoio(db["cats"].get(str(a)), str(a), {}, db)
    if bot.user is not None:
        if a == bot.user.id:
            return
    if c == "cat":
        if gid == 0 or message.guild is None:
            await message.reply("sureeeeee")
            return
        ctype_guild = tevcnoio(db["cattype"].get(str(gid)), str(gid), {}, db["cattype"])
        ctype: str = tevcnoio(ctype_guild.get(str(cid)), str(cid), "none", ctype_guild)
        if ctype == "none":
            await message.reply("har har har you said cat")
        else:
            # print(ctype)
            tevcnoio(adb.get(ctype), ctype, 0, adb)
            adb[ctype] += 1
            # print(adb)
            db["cats"].update({a: adb})
            # print(db, db["cats"])
            db.save("cats")
            await message.delete()
            cmsg = setup_tasks[cid].current_msg
            if cmsg is not None:
                await cmsg.delete()
                setup_tasks[cid].cat_active = False
            emoji = nc.utils.get(message.guild.emojis, name=ctype + "cat")
            await message.channel.send(
                f" \
{message.author.display_name} cought {emoji} {ctype.capitalize()} cat!!!!1!\n\
You now have {adb[ctype]} cats of dat type!!!\n\
this fella was cought in (uhh idk) seconds!!!!"
            )
            db["cattype"][str(gid)][str(cid)] = "none"
            # await message.channel.send(f"You now have {adb[ctype]} {ctype} cats!!")
        # await message.channel.send("oki i will now gib free fine cat!")
        # update_json(
        #     {"fine": 1},
        #     "data/cats.json",
        #     {a: try_get(load_json("data/cats.json"), str(a), {})},
        # )
    if c == "r":
        if message.author.name == "frinkifail":
            await message.reply("oki restarting")
            if db["cattype"] is not None:
                db.save("cattype")
            else:
                print("cat type is none lol")
            execv(executable, ["python"] + argv)
        else:
            await message.reply("skill issue")
    await handle_ach(message, c, message.author)


# @bot.slash_command('say', 'make the bot say something')
# async def say(interaction: nc.Interaction, what: str): await cmd_say(interaction, what)

bot.run(read_file("dev/TOKEN.txt"))
