#!/Users/waadna/.pyenv/shims/python
from os import execv
from sys import argv, executable
from typing import Any, Optional
import nextcord as nc
from nextcord.ext import commands
from code_resources.command_achivement import achivement_cb
from code_resources.command_forget import forget_cb
from code_resources.command_inventory import inventory_cb
from code_resources.command_setup import setup_cb
from code_resources.handle_achs import handle_ach
from code_resources.handle_catch import catch_cb
from code_resources.utility.cat_run_task import CatLoop
from code_resources.utility.util import (
    db,
    init_data,
    read_file,
)

init_data()

bot = commands.Bot(intents=nc.Intents.all())

setup_tasks: dict[int, CatLoop] = {}  # ChannelID: Loop
cscwg: dict[
    int, list[int]
] = {}  # Current Setup Channels With Guild # {GuildID: [ChannelID, ...]}

RESTART_LOG = 1154694509494550568

# region Events


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user.global_name}")
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


@bot.event
async def on_message(message: nc.Message):
    c = message.content
    a = message.author.id
    gid = (
        message.guild.id if message.guild else 0
    )  # smhhhh null checks for example they send in dms or smthhhh
    cid = message.channel.id
    adb: dict[str, Any] = db.uget(a, "cats")
    if bot.user is not None:
        if a == bot.user.id:
            return
    if c == "cat":
        await catch_cb(message, gid, cid, adb, setup_tasks, a)
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


# endregion

# region Slash Commands


@bot.slash_command("setup", "setup the bot")
async def setup(interaction: nc.Interaction):
    await setup_cb(interaction, setup_tasks)


@bot.slash_command("forget", "i forgor :skull: (unsetup)")
async def forgor(interaction: nc.Interaction):
    await forget_cb(interaction, setup_tasks)


@bot.slash_command("inventory", "see your or other's inventory")
async def inventory(interaction: nc.Interaction, person: Optional[nc.User]):
    await inventory_cb(interaction, person, bot)


@bot.slash_command("achivements", "see how many achivements you have")
async def achivement(interaction: nc.Interaction):
    await achivement_cb(interaction)


# endregion

bot.run(read_file("dev/TOKEN.txt"))
