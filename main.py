import nextcord
from nextcord.ext import commands
from code_resources.command_say import cmd_say

from code_resources.utility.util import read_file

bot = commands.Bot()

@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user.display_name}")
    else:
        print("Not logged in (how?)")

@bot.slash_command('say', 'make the bot say something')
async def say(interaction: nextcord.Interaction, what: str): await cmd_say(interaction, what)

bot.run(read_file('dev/TOKEN.txt'))
