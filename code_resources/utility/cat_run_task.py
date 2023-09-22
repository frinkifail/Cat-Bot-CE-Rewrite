from asyncio import Task, create_task, sleep
from random import randint, random
from typing import TypedDict

from discord import File, Interaction
from discord.utils import get

from code_resources.utility.util import load_json

# region Cat Chances
# Modify the `TypedDict` containing chances types to add new cats.
# For example,
"""
...:
    silly: float,
    spagetti: float
"""
# and then,
"""
cat_chances: CatChances = {
    silly: 20, # Percent of spawning here
    spagetti: 50
}
"""


class CatChances(TypedDict):  # Makes it easier (autocomplete)
    fine: float
    nice: float
    good: float
    rare: float
    wild: float
    baby: float
    epic: float
    sus: float
    brave: float
    rickroll: float
    reverse: float
    superior: float
    the_trash_cell: float
    legendary: float
    _8bit: float
    corrupt: float
    professor: float
    divine: float
    real: float
    ultimate: float
    egirl: float


cat_chances: CatChances = {  # Ripped straight from my good friend milenakosa.
    # I like how most of them are sorted in alphabetical order lmao
    "fine": 24.34,
    "nice": 18.25,
    "good": 12.17,
    "rare": 8.51,
    "_8bit": 0.48,
    "baby": 5.59,
    "brave": 3.65,
    "corrupt": 0.36,
    "divine": 0.19,
    "egirl": 0.04,
    "epic": 4.86,
    "legendary": 0.85,
    "professor": 0.24,
    "real": 0.12,
    "reverse": 2.43,
    "rickroll": 3.04,
    "superior": 1.94,
    "sus": 4.25,
    "the_trash_cell": 1.21,
    "ultimate": 0.07,
    "wild": 6.69,
}
# endregion


class CatLoop:
    def __init__(
        self,
        interaction: Interaction,
        loopid: str | int,
        guild_id: int,
        channel_id: int,
    ) -> None:
        self.id = loopid
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.task: Task | None = None
        self.running: bool = False
        self.interaction = interaction
        self.cat_active = False

    async def start(self):
        if not self.running:
            self.task = create_task(
                self._loop(),
                name=f"Spawn loop for {self.channel_id} ({self.guild_id}) also known as {self.id}",
            )
            self.running = True
            return True
        else:
            print("Loop is already running you bozo!")
            return False

    async def _loop(self):
        # Get JSON data from 'data/timings.json' and get the value of key {self.guild_id}
        json_data: dict[int, float] = load_json("data/timings.json")
        data = json_data.get(self.guild_id)
        if data is None:
            print(
                "[WARNING] This guild doesn't have a timing data key. Defaulting to 2."
            )
            await self.interaction.send("No timing set, using 2 seconds.")
            data = 2
        while self.running:
            if not self.running:
                break
            await sleep(data)
            spawn_cat_or_no = randint(0, 100)
            if (
                30 <= spawn_cat_or_no <= 95 and not self.cat_active
            ):  # yay we spawn cat now
                cat_type = "fine"
                chance = random() * 100
                for k, c in cat_chances.items():
                    # So, why didn't just use type: ignore the first time you may ask?
                    # Because, uhm
                    # haha typecheck go brrrrr
                    try:
                        # shuddup pyright
                        v = float(c)  # type: ignore
                    except ValueError as e:
                        print(f"[ERROR] Error in loop {self.id}: {e}")
                        v = -1.0
                    if chance < v:
                        cat_type = k
                if cat_type == "_8bit":
                    cat_type = "8bit"
                if self.interaction.guild is not None:
                    self.cat_active = True
                    emoji = get(
                        self.interaction.guild.emojis, name=cat_type.lower() + "cat"
                    )
                    emojistr = emoji.__str__()
                    # self.interaction.send(emojistr)
                    await self.interaction.send(
                        f"guys!! {cat_type} apered! {emojistr}",
                        file=File("code_resources/staring.png"),
                    )
