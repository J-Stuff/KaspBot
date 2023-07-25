import discord, logging, os, datetime
from discord.ext import commands
from enum import Enum, IntEnum, EnumMeta, StrEnum
from src.functions.verification import VerificationView

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

# Enum Fuckery

# Bot Info
class Info(StrEnum):
    AUTHOR = 'jstuff'
    VERSION = '2.0.0 - PRE-ALPHA 0'
    SOURCE = 'https://github.com/J-Stuff/KaspBot'
    DEVELOPMENT = True


# Bot Guilds
class Guilds(IntEnum):
    MAIN = 1038438846104338473
    DEV = 1038684902901678150

class _MAIN_Roles(IntEnum):
    OWNER = 1038448231715197058
    CO_OWNER = 1059965540447301642
    KASPBOT = 1040491274949636139
    BOT_MASTER = 1039595996071612477
    STAFF = 1038448580224094329
    BOTS = 1077383482357071994

    # REACTION ROLES vvv
    RED = 1038448847900381204
    ORANGE = 1038448895052759152
    YELLOW = 1038449003051884574
    GREEN = 1038449068512387154
    TEAL = 1038449821419319419
    FOREST_GREEN = 1107117755943100466
    CYAN = 1038449877786558535
    BLUE = 1038449923697410068
    PURPLE = 1038450034238304267
    PINK = 1038450355974971463

    # UTILITIES vvv
    BOOSTER = 1038599988353171487
    MEMBER = 1038451098748465162
    ARTIST = 1041946134010146837
    NSFW = 1038460667776213024
    DEGENERATE = 1038471815976194129
    UNVERIFIED = 1048806955684221028


    # REACTION ROLES VVV
    # SPECIES vvv
    AVIAN = 1077517329358917694
    BEAR = 1077517425895034911
    CANINE = 1077517538725998692
    DEER = 1077517604828229643
    DERG = 1077517661916897370
    DRAGON = 1077517723258605579
    FELINE = 1077517790237429790
    FOX = 1077517851814019142
    HOBKIN = 1077517914497896448
    KOBOLD = 1077517977781538866
    MOTH = 1077518068814712882
    OTTER = 1077518141950787654
    PROTOGEN = 1077518195046490174
    SHARK = 1077518242605699164
    SERGAL = None
    SKULLDOG = 1077518292073336883
    WICKERBEAST = 1077518370125119570

    # ORIENTATION vvv
    ASEXUAL = 1038627791899463762
    BISEXUAL = 1038627319398539364
    GAY = 1038627056436654150
    LESBIAN = 1038627517453578280
    PANSEXUAL = 1038627657472020490
    STRAIGHT = 1038626750839656449

    # GENDER vvv
    MALE = 1077518550736048169
    DEMI = 1084247384529322055
    FEMALE = 1077518632495628288
    NON_BINARY = 1077518703664566292

    # PRONOUNS vvv
    HE_HIM = 1077519339533647974
    SHE_HER = 1077519307426254858
    THEY_THEM = 1077519392977457183
    ANY_PRONOUNS = 1077519478314762280
    OTHER_PRONOUNS = 1077519511298773042

    # OTHER vvv


class _MAIN_Channels(IntEnum):
    # ANNOUNCMENETS vvv
    ANNOUNCMENTS = 1038460073451737098
    TT_EVENTS = 1038678573457870868
    TT_UPLOADS = 1068071672600612914

    # FRONT DOOR vvv
    RULES = 1038444518128758804
    WELCOME_MAT = 1038443763644768256
    VERIFICATION = 1077522456362897498
    UNVERIFIED = 1077520917518880879
    CHANNELS_INTRO = 1041953458154131476
    REACTION_ROLES = 1040493199388590110

    # EXTRAS vvv
    SUGGESTIONS = 1041131126367981748
    MOVIE_SUGGESTIONS = 1051393184640552970

    # INTROS vvv
    PERSONAL_INTROS = 1114507985566318623
    SONA_INTROS = 1114508082031099967

    # BOOSTER vvv
    BOOSTER_CHAT = 1047794210771836978
    BOOSTER_MEMES = 1047794673583915049
    BOOSTER_ART = 1047795642954698754
    BOOSTER_SONAS = 1047796395974869002
    BOOSTER_VOICE = 1047795879878332426

    # GENERAL vvv
    MAIN = 1038438847534600255
    MAIN2 = 1038458237273522246
    BOT_COMMANDS = 1091292509528928287
    MEDIA = 1054601529941831700
    FORUMS = 1091301575659638835
    RP = 1054435974765097012
    MEMES = 1038660793966800906
    NO_CONTEXT = 1051389751904706631
    GAMING = 1038457158397874318
    MUSIC = None
    VEHICLE = None
    TECH = None
    PETS = None
    FOOD = None
    VENTING = None

    # ART vvv
    ART_TALK = None
    FLOOFY_ART = None
    SONA_ART = None
    COMMISSIONS = None
    COMMISSIONS_COMPLETED = None

    # NSFW TO BE ADDED WHEN THE BOT INTERACTS WITH IT
    # DEGENERATE TO BE ADDED WHEN THE BOT INTERACTS WITH IT

    # VOICE vvv
    GENERAL_VOICE = 1038438847534600256
    GAMING_VOICE = 1051390498742485092
    MOVIE_VOICE = 1051391251162878042
    IDLE_VOICE = 1085105997011497010

    # MODERATION vvv
    STAFF_ANNOUNCEMENTS = 1054997481676611684
    STAFF_INTRO = 1054989167882420224
    STAFF_CHAT = 1040490657850077184
    VERIFICATION_LOGGING = 1077519987029311549
    USER_LOGS = 1040488068571992094
    ADMIN_LOGS = 1040488111999828039
    ATTACHMENT_LOGS = 1128267884704043018
    COMMAND_LOGS = 1040488091317706883
    SYSTEM_MESSAGES = 1058101998190350466
    TICKET_LOGS = 1047766100760342600
    BOT_LOGS = 1085313363178946610

class _DEV_Channels(IntEnum):
    TESTING_ANNOUNCEMENTS = 1085340072494256198
    BACKUP_LOGS = 1128217174373306388

class _DEV_Roles(IntEnum):
    pass
class MainGuild(Enum):
    ROLES = _MAIN_Roles
    CHANNELS = _MAIN_Channels


class DevGuild(Enum):
    ROLES = _DEV_Roles
    CHANNELS = _DEV_Channels

# End of ENUM Fuckery

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
    'src.commands.about',
    'src.commands.boop',
    'src.functions.status',
    'src.functions.attachmentLogging',
    'src.commands.unverified_purge',
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
        self.CogList = Cogs
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
        self.add_view(VerificationView(self))
        logging.info(f'Logged in as {self.user.name} - {self.user.id}') #type:ignore
        logging.info(f'Version: {discord.__version__}')
        logging.info('------')
