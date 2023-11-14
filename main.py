#!python
from os import execv
from sys import argv, executable
from typing import Any, Optional
import nextcord as nc
from nextcord.ext import commands
import code_resources as cr

cr.init_data()

bot = commands.Bot(intents=nc.Intents.all())

setup_tasks: dict[int, cr.CatLoop] = {}  # ChannelID: Loop
cscwg: dict[
    int, list[int]
] = {}  # Current Setup Channels With Guild # {GuildID: [ChannelID, ...]}

RESTART_LOG = 1151851013637152859
OWNER_USERNAME = "frinkifail"

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
            # TODO (Complete): setup for everything in db[cscwg]
            for k, v in cr.db["cscwg"].items():
                k: int  # Explicit typing
                v: list[int]
                guild = await bot.fetch_guild(k)
                channels: list[nc.guild.GuildChannel | nc.Thread] = []
                for i in v:
                    channel = await guild.fetch_channel(i)
                    channels.append(channel)
                for i in channels:
                    if isinstance(i, nc.TextChannel):
                        setup_tasks[i.id] = cr.CatLoop(i, guild, 0)
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
    if bot.user is not None:
        if a == bot.user.id:
            return
    if c == "cat":
        adb: dict[str, Any] = cr.db.uget(a, "cats")
        await cr.catch_cb(message, gid, cid, adb, setup_tasks, a)
    if c == "r":
        if message.author.name == "frinkifail":
            await message.reply("oki restarting")
            if cr.db["cattype"] is not None:
                cr.db.save("cattype")
            else:
                print("cat type is none lol")
            execv(executable, ["python"] + argv)
        else:
            await message.reply("restart failed: not bot owner")
    if c.startswith("kat>"):
        d = c.replace("kat>", "").split(maxsplit=2)
        if message.author.name == OWNER_USERNAME:
            admin = True
        else:
            admin = False
        await cr.handle_debug(bot, message, admin, d[0], d[1].split())
    await cr.handle_ach(message, c, message.author)


# endregion

# region Slash Commands


@bot.slash_command("setup", "setup the bot")
async def setup(interaction: nc.Interaction):
    await cr.setup_cb(interaction, setup_tasks)


@bot.slash_command("forget", "i forgor :skull: (unsetup)")
async def forgor(interaction: nc.Interaction):
    await cr.forget_cb(interaction, setup_tasks)


@bot.slash_command("inventory", "see your or other's inventory")
async def inventory(interaction: nc.Interaction, person: Optional[nc.User]):
    await cr.inventory_cb(interaction, person, bot)


@bot.slash_command("achivements", "see how many achivements you have")
async def achivement(interaction: nc.Interaction):
    await cr.achivement_cb(interaction)


@bot.slash_command(
    "forcespawn", "i mean, pretty self-explanatory. it just spawns a cat"
)
async def forcespawn(interaction: nc.Interaction, force: bool = False):
    if (
        not isinstance(interaction.channel, nc.TextChannel)
        or not interaction.channel_id
        or not interaction.guild
        or not interaction.guild_id
    ):
        await interaction.send("ong seriously")
        return
    catloop = setup_tasks.get(interaction.channel_id)
    if catloop is None:
        await interaction.send("this channel isn't even setup")
        return
    if catloop.cat_active and not force:
        await interaction.send(
            "there's already a cat sitting around; if there's no cat; use the `force` parameter."
        )
        return
    await catloop.spawn()
    await interaction.send("done!")


# endregion

bot.run(cr.read_file("dev/TOKEN.txt"))
