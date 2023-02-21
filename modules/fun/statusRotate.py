import json
import os
import sys
import random
import discord
import logging
from config.getSetting import getSetting
from discord.ext import commands

async def funStatus(bot:commands.Bot):
    from pymongo import MongoClient
    CONNECTION_STRING = os.getenv("MONGO_connection_string")
    client: MongoClient = MongoClient(CONNECTION_STRING)
    database = os.getenv("MONGO_maindb")
    if database == None:
        logging.info("BAD ENV MONGO_maindb")
        sys.exit()
    
    db = client[database]

    collection = getSetting("MONGO_status_collection")
    if collection == None:
        logging.info("BAD DB MONGO_verification_collection")
        sys.exit()
        
    statusStore = db[collection]
    statusMessages = list(statusStore.find({}))
    
    newStatus = statusMessages[random.randint(0, (len(statusMessages)-1))]

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

    await bot.change_presence(status=discord.Status.online, activity=statusMsg)  # type: ignore