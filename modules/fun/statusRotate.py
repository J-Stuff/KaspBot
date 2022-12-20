import json
import random
import discord

async def funStatus(bot):
    with open('./resources/statusMessages.json', 'r') as fp:
        statusMessages = json.loads(fp.read())
    
    newStatus = statusMessages[str(random.randint(0, 15))]

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