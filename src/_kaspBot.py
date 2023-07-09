import discord, logging, os, datetime
from discord.ext import commands
from enum import IntEnum, StrEnum, Enum

if __name__ in "__main__":
    print("This file is not meant to be run directly. Please run bootloader.py instead.")
    exit(1)

# Archive old logs
if os.path.exists('./logs/kaspBot.log.old'):
    os.remove('./logs/kaspBot.log.old')

if os.path.exists('./logs/kaspBot.log'):
    os.rename('./logs/kaspBot.log', './logs/kaspBot.log.old')

# Logging
logging.basicConfig(level=logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler('./logs/kaspBot.log')
Logger = logging.getLogger()
Logger.addHandler(stream_handler)


# Bot Guilds
class Guilds(IntEnum):
    MAIN = 1038438846104338473
    DEV = 1038684902901678150

class MainGuild(Enum):
    ID = 1038438846104338473
    class Roles(IntEnum):
        pass

    class Channels(IntEnum):
        pass

class DevGuild(Enum):
    ID = 1038684902901678150
    class Roles(IntEnum):
        pass

    class Channels(IntEnum):
        pass

# Bot Statuses
StatusList = [
    {'name': 'the cries of the locked up children', type: discord.ActivityType.listening},
    {'name': 'the cries of the damned', type: discord.ActivityType.listening},
    {'name': 'games with the devil', type: discord.ActivityType.playing},
    {'name': 'nuclear warhead testing', type: discord.ActivityType.streaming},
    {'name': 'zoomies', type: discord.ActivityType.playing},
    {'name': 'with the FBI', type: discord.ActivityType.playing},
    {'name': 'fortunate son', type: discord.ActivityType.listening},
    {'name': 'Kasper\'s financial crisis', type: discord.ActivityType.watching},
]

# Bot Cogs
Cogs = [
    'commands.about',
]

# Bot Info
class Info(StrEnum):
    AUTHOR = 'jstuff'
    VERSION = '2.0.0'
    SOURCE = 'https://github.com/J-Stuff/KaspBot'

# Bot Cog loader
async def load_cogs(bot: commands.Bot):
    logging.info('Loading cogs')
    for cog in Cogs:
        logging.info(f'Loading {cog}')
        await bot.load_extension(cog)
        logging.info(f'Loaded {cog}')

# Misc Functions/Events to run

now = datetime.datetime.now()
logging.info("Bot started at " + now.strftime("%Y-%m-%d %H:%M:%S"))

# Bot object
class KaspBot(commands.Bot):
    def __init__(self):
        self.uptime = now
        self.info = Info
        self.EnumGulds = Guilds
        self.EnumMainGuild = MainGuild
        self.EnumDevGuild = DevGuild
        super().__init__(command_prefix=';', intents=discord.Intents.all(), help_command=None)

    # Bot on ready
    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name} - {self.user.id}') #type:ignore
        logging.info(f'Version: {discord.__version__}')
        logging.info('------')
