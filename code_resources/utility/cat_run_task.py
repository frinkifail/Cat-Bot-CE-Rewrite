from asyncio import Task, create_task, sleep
from random import randint, random
from time import time
from typing import TypedDict

from discord import File, Guild, Message, TextChannel
from discord.utils import get

from code_resources.utility.util import load_json, db, timings

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
        channel: TextChannel,
        guild: Guild,
        loopid: str | int,
    ) -> None:
        self.id = loopid
        self.task: Task | None = None
        self.running: bool = False
        self.cat_active = False
        self.current_msg: Message | None = None
        self.channel = channel
        self.guild = guild

    async def start(self):
        if not self.running:
            self.task = create_task(
                self._loop(),
                name=f"Spawn loop for {self.channel.id} ({self.guild.id}) also known as {self.id}",
            )
            self.running = True
            print(f"succesfully started {self.id}")
            return True
        else:
            print(f"loop is already running you bozo ({self.id})")
            return False

    async def _loop(self):
        # Get JSON data from 'data/timings.json' and get the value of key {self.guild_id}
        # json_data: dict[int, float] = load_json("data/timings.json")
        data: float = timings.reload().get(self.guild.id, {}).get(self.channel.id, 5)
        if data is None:
            print(
                "[WARNING] This guild doesn't have a timing data key. Defaulting to 5."
            )
            # await self.channel.send("No timing set, using 2 seconds.")
            data = 5
            # db["timings"][self.guild.id][self.channel.id] = 5
            # timings.get(self.guild.id, {})[self.channel.id] = 5
            # db.save("timings")
            timings.save()
        print(f"ok opened loop for {self.id}")
        while self.running:
            if not self.running:
                print(f"oki closing loop for {self.id}")
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
                self.cat_active = True
                emoji = get(self.guild.emojis, name=cat_type.lower() + "cat")
                db["cattype"][str(self.guild.id)][str(self.channel.id)] = cat_type
                # db["times"][str(self.guild.id)][str(self.channel.id)] = time()
                if db["times"].get(self.guild.id) is None:
                    db["times"][self.guild.id] = {}
                db["times"][self.guild.id][self.channel.id] = time()
                db.save('times')
                self.current_msg = await self.channel.send(
                    f'{emoji} A {cat_type.capitalize()} cat appeared! Type "cat" to catch it!',
                    file=File("code_resources/staring.png"),
                )
