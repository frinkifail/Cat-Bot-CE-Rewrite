from __future__ import annotations
from random import choice
from typing import TYPE_CHECKING
from git import Repo

if TYPE_CHECKING:
    from discord import Message
    from nextcord.ext.commands import Bot


PING_SPLASHES = [
    "http://sussy",
    "hewwo",
    "ok and",
    "woah",
    "cool",
    "pinged",
    "pong",
    "H",
    "hello, world!",
    "staring cat",
    "hmm",
    "okay",
    "this splash is sponsered by",
    "cat bot is cool",
    "milenakosa",
    "this splash is sponsered by... wait why do i feel like this splash was here before...",
    "this splash is sponsered by ummmm",
    "hashtag talk",
    "cool people chat",
    "i loveeee rewriting cat bot",
    "well i dont",
]


async def handle_debug(
    bot: "Bot", msg: "Message", is_owner: bool, command: str, args: list[str]
):
    if command == "ping":
        repo = Repo(search_parent_directories=True)
        await msg.reply(
            f"""
{choice(PING_SPLASHES)} ({round(bot.latency * 1000)}ms)
Version: {repo.head.object.hexsha}
        """
        )
        del repo
