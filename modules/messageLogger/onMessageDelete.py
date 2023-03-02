import time
import discord
import os
import logging
from discord.ext import commands
from config.getConfig import settings as unsettings
settings = unsettings()

async def onMessageDelete(message:discord.Message, bot:commands.Bot):
    logging.info(f"Message Deleted: {message.content}")
    if message.author.id == bot.user.id or message.content == None: #type:ignore
        return
    unix = int(time.time())
    embed = discord.Embed(title="A message was Deleted!",
                          description=f"Deleted in: <#{message.channel.id}>\nAt <t:{unix}:T>", color=discord.colour.parse_hex_number("ff0000"))
    embed.add_field(name="Message Content:", value=f"```{message.content}```", inline=False)
    if message.attachments:
        embed.add_field(name="Attachments", value=message.attachments, inline=False)
    embed.set_author(
        name=f"{message.author} ({message.author.id})", icon_url=message.author.avatar)
    channel = bot.get_channel(int(settings.getChannelID("messageLogs")))
    await channel.send(embed=embed)   # type: ignore
