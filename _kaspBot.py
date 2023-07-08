import discord
from discord.ext import commands
from enum import IntEnum


# Bot prefix
class KaspBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=';', intents=discord.Intents.all())

    # Bot on ready
    async def on_ready(self):
        print(f'Logged in as {self.user.name} - {self.user.id}') #type:ignore
        print(f'Version: {discord.__version__}')
        print('------')


# Bot status
class Status(IntEnum):
    OFFLINE = 0
    ONLINE = 1
    IDLE = 2
    DND = 3
    INVISIBLE = 4
    