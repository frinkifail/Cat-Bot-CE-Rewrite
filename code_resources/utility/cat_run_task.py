from asyncio import Task, create_task, sleep


class CatLoop:
    def __init__(self, loopid: str | int, guild_id: int, channel_id: int) -> None:
        self.id = loopid
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.task: Task | None = None
        self.running: bool = False
    async def start(self):
        if not self.running:
            self.task = create_task(self._loop(), name=f"Spawn loop for {self.channel_id} ({self.guild_id})")
            self.running = True
            return True
        else:
            print("Loop is already running you bozo!")
            return False
    async def _loop(self):
        while self.running:
            if not self.running:
                break
            await sleep(1)
