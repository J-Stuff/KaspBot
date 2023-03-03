import logging
from discord.ext import commands, tasks
import discord
import random
import json

class Loop(commands.Cog, name="Loop cogs"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.do_funStatus.start()

    @tasks.loop(minutes=2)
    async def do_funStatus(self):
        logging.debug("Rotating bot custom status")
        logging.debug("Reading status DB")
        with open("./database/status.json", 'r') as fp:
            logging.debug("Parsing JSON")
            statusList = json.load(fp)
            fp.close()

        logging.debug("Picking a new status")
        newStatus = random.choice(statusList)
        logging.debug(f"Using status: {newStatus}")

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

        logging.debug("Rotating presence now...")
        await self.bot.change_presence(status=discord.Status.online, activity=statusMsg)

    @do_funStatus.before_loop
    async def beforeLogin(self):
        logging.info("Waiting for websocket")
        await self.bot.wait_until_ready()

async def setup(bot:commands.Bot):
    logging.info(f"{__file__} - Setting up...")
    await bot.add_cog(
        Loop(bot)
    )
    logging.info(f"{__file__} - Done!")