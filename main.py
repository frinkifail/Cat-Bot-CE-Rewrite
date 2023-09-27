#!/Users/waadna/.pyenv/shims/python
from os import execv
from sys import argv, executable
from typing import Any, Optional
import nextcord as nc
from nextcord.ext import commands
from code_resources.command_inventory import inventory_cb
from code_resources.command_setup import setup_cb
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

RESTART_LOG = 1154694509494550568


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user.display_name}")
        await bot.change_presence(
            activity=nc.Activity(type=nc.ActivityType.playing, name="with Cat Bot"),
            status=nc.Status.dnd,
        )
        catbot_channel = await bot.fetch_channel(RESTART_LOG)
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
    await setup_cb(interaction, setup_tasks)


@bot.slash_command("inventory", "see your or other's inventory")
async def inventory(interaction: nc.Interaction, person: Optional[nc.User]):
    await inventory_cb(interaction, person, bot)


@bot.event
async def on_message(message: nc.Message):
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
            emoji = nc.utils.get(message.guild.emojis, name=ctype + "cat")
            await message.channel.send(
                f" \
{message.author.display_name} cought {emoji} {ctype.capitalize()} cat!!!!1!\n\
You now have {adb[ctype]} cats of dat type!!!\n\
this fella was cought in (uhh idk) seconds!!!!"
            )
            db["cattype"][str(gid)][str(cid)] = "none"
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
