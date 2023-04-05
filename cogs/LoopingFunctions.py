from discord.ext import commands, tasks
import discord
import random
import json
import logging
logger = logging.getLogger('kaspbot')

class Loop(commands.Cog, name="Loop cogs"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.do_funStatus.start()

    @tasks.loop(minutes=2)
    async def do_funStatus(self):
        logger.debug("Rotating bot custom status")
        logger.debug("Reading status DB")
        with open("./database/status.json", 'r') as fp:
            logger.debug("Parsing JSON")
            statusList = json.load(fp)
            fp.close()

        logger.debug("Picking a new status")
        newStatus = random.choice(statusList)
        logger.debug(f"Using status: {newStatus}")

        if newStatus["type"] == "playing":
            statusMsg = discord.Game(name=newStatus["content"])
        elif newStatus["type"] == "streaming":
            statusMsg = discord.Streaming(name=newStatus["content"], url="https://discord.com/channels/1038438846104338473/1038460073451737098")
        elif newStatus["type"] == "listening":
            statusMsg = discord.Activity(type=discord.ActivityType.listening, name=newStatus["content"])
        elif newStatus["type"] == "watching":
            statusMsg = discord.Activity(type=discord.ActivityType.watching, name=newStatus["content"])
        else:
            statusMsg = discord.Game(name="in a virtual paradise")

        logger.debug("Rotating presence now...")
        await self.bot.change_presence(status=discord.Status.online, activity=statusMsg)

    @do_funStatus.before_loop
    async def beforeLogin(self):
        logger.info("Waiting for websocket")
        await self.bot.wait_until_ready()

async def setup(bot:commands.Bot):
    logger.info(f"{__file__} - Setting up...")
    await bot.add_cog(
        Loop(bot)
    )
    logger.info(f"{__file__} - Done!")