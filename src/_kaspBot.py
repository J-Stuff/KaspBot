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

# Bot Info
class Info(StrEnum):
    AUTHOR = 'jstuff'
    VERSION = '2.0.0'
    SOURCE = 'https://github.com/J-Stuff/KaspBot'
    DEVELOPMENT = True


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
    discord.Activity(name='the cries of the locked up children', type=discord.ActivityType.listening),
    discord.Activity(name='the screams of the damned', type=discord.ActivityType.listening),
    discord.Activity(name='the sound of silence', type=discord.ActivityType.listening),
    discord.Activity(name='games with the devil', type=discord.ActivityType.playing),
    discord.Activity(name='with the devil', type=discord.ActivityType.playing),
    discord.Activity(name='nuclear warhead testing', type=discord.ActivityType.streaming),
    discord.Activity(name='zoomies', type=discord.ActivityType.playing),
    discord.Activity(name='with the FBI', type=discord.ActivityType.playing),
    discord.Activity(name='fortunate son', type=discord.ActivityType.listening),
    discord.Activity(name='Kasper\'s financial crisis', type=discord.ActivityType.watching),
    discord.Activity(name='guess the speed limit', type=discord.ActivityType.playing),
    discord.Activity(name='you call Kasper stimky', type=discord.ActivityType.listening),
    discord.Activity(name='with my tail', type=discord.ActivityType.playing),
    discord.Activity(name='your every move', type=discord.ActivityType.watching),
    discord.Activity(name='... no wait I\'m not listening to you', type=discord.ActivityType.listening),
    discord.Activity(name='your conversations', type=discord.ActivityType.watching),
    discord.Activity(name='with my paw beans', type=discord.ActivityType.playing),
    discord.Activity(name='to Kasper yell at his Truck', type=discord.ActivityType.listening),
    discord.Activity(name='Kasper\'s latest TikTok', type=discord.ActivityType.watching),
    discord.Activity(name='you', type=discord.ActivityType.watching),
    discord.Activity(name='with my toys', type=discord.ActivityType.playing),
    discord.Activity(name='with my food', type=discord.ActivityType.playing),
    discord.Activity(name='with my megaphone', type=discord.ActivityType.playing),
]

# Bot Cogs
Cogs = [
    'commands.about',
    'functions.status',
]



# Bot Cog loader
async def load_cogs(bot: commands.Bot):
    logging.info('Loading cogs')
    for cog in Cogs:
        logging.info(f'Loading {cog}')
        await bot.load_extension(cog)
        logging.info(f'Loaded {cog}')
    logging.info('Loaded cogs')

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
        self.statuses = StatusList
        super().__init__(command_prefix=';', intents=discord.Intents.all(), help_command=None)

    # Setup
    async def setup_hook(self):
        logging.info('Setting up bot')
        await load_cogs(self)
        logging.info('Bot setup complete')
        return await super().setup_hook()

    # Bot on ready
    async def on_ready(self):
        logging.info(f'Logged in as {self.user.name} - {self.user.id}') #type:ignore
        logging.info(f'Version: {discord.__version__}')
        logging.info('------')
