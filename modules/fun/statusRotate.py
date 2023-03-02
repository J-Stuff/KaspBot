import json
import random
import discord
import logging
from discord.ext import commands

async def funStatus(bot:commands.Bot):
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
    await bot.change_presence(status=discord.Status.online, activity=statusMsg)