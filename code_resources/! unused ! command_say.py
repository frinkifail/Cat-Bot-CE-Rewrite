from discord import Interaction


async def cmd_say(interaction: Interaction, what: str):
    await interaction.send(what)
