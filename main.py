#!/Users/waadna/.pyenv/shims/python
from os import execv
from sys import argv, executable
import nextcord
from nextcord.ext import commands
from code_resources.utility.cat_run_task import CatLoop

# from code_resources.! unused ! command_say

from code_resources.utility.util import (
    init_data,
    load_json,
    read_file,
    save_json,
    try_get,
    update_json,
)

init_data()

bot = commands.Bot(intents=nextcord.Intents.all())


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user.display_name}")
    else:
        print("Not logged in (how?)")


@bot.slash_command("setup", "setup the bot")
async def setup(interaction: nextcord.Interaction):
    if interaction.guild is not None and interaction.channel is not None:
        something = CatLoop(
            interaction, 0, interaction.guild.id, interaction.channel.id
        )
        await something.start()
    else:
        await interaction.send("ok smth went insanely wrong")


@bot.event
async def on_message(message: nextcord.Message):
    # print("on message")
    # print(message)
    c = message.content
    a = message.author.id
    # print(c)
    if bot.user is not None:
        if a == bot.user.id:
            return
    if c == "cat":
        await message.reply("har har you said cat")
        await message.channel.send("oki i will now gib free fine cat!")
        update_json(
            {"fine": 1},
            "data/cats.json",
            try_get(load_json("data/cats.json"), str(a), {}),
        )
    if c == "r":
        if message.author.name == "frinkifail":
            await message.reply("oki restarting")
            execv(executable, ["python"] + argv)
        else:
            await message.reply("skill issue")


# @bot.slash_command('say', 'make the bot say something')
# async def say(interaction: nextcord.Interaction, what: str): await cmd_say(interaction, what)

bot.run(read_file("dev/TOKEN.txt"))
