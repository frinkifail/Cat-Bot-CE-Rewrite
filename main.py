#!/Users/waadna/.pyenv/shims/python
from os import execv
from sys import argv, executable
from typing import Any, Optional
import nextcord as nc
from nextcord.ext import commands
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


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user.display_name}")
        catbot_channel = await bot.fetch_channel(1151851013637152859)
        if isinstance(catbot_channel, nc.TextChannel):
            await catbot_channel.send("oki i restarted")
    else:
        print("Not logged in (how?)")


@bot.slash_command("setup", "setup the bot")
async def setup(interaction: nc.Interaction):
    if interaction.guild is not None and interaction.channel is not None:
        cid = interaction.channel.id
        setup_tasks[cid] = CatLoop(interaction, 0, interaction.guild.id, cid)
        await setup_tasks[cid].start()
    else:
        await interaction.send("ok smth went insanely wrong")


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
        if gid == 0:
            await message.reply("sureeeeee")
            return
        ctype_guild = tevcnoio(db["cattype"].get(str(gid)), str(gid), {}, db["cattype"])
        ctype = tevcnoio(ctype_guild.get(str(cid)), str(cid), "none", ctype_guild)
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
            await message.channel.send(
                f"{message.author.display_name} caught {ctype} in (haha my current intelligence level is not to the level of knowing how long it took)!!"
            )
            await message.channel.send(f"You now have {adb[ctype]} {ctype} cats!!")
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


# @bot.slash_command('say', 'make the bot say something')
# async def say(interaction: nc.Interaction, what: str): await cmd_say(interaction, what)

bot.run(read_file("dev/TOKEN.txt"))
