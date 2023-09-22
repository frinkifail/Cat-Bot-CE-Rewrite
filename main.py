from discord import Interaction
import nextcord
from nextcord.ext import commands
from code_resources.utility.cat_run_task import CatLoop

# from code_resources.! unused ! command_say

from code_resources.utility.util import init_data, read_file

init_data()

bot = commands.Bot()


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user.display_name}")
    else:
        print("Not logged in (how?)")


@bot.slash_command("setup", "setup the bot")
async def setup(interaction: Interaction):
    if interaction.guild is not None and interaction.channel is not None:
        something = CatLoop(
            interaction, 0, interaction.guild.id, interaction.channel.id
        )
        await something.start()
    else:
        await interaction.send("ok smth went insanely wrong")


# @bot.slash_command('say', 'make the bot say something')
# async def say(interaction: nextcord.Interaction, what: str): await cmd_say(interaction, what)

bot.run(read_file("dev/TOKEN.txt"))
