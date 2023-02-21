import time
import discord
import os
import logging
from config.getSetting import getSetting

async def onMessageDelete(message, bot):
    logging.info(f"Message Deleted: {message.content}")
    if message.author.id == bot.user.id or message.content == None:  
        return

    unix = int(time.time())
    embed = discord.Embed(title="A message was Deleted!",
                          description=f"Deleted in: <#{message.channel.id}>\nAt <t:{unix}:T>", color=discord.colour.parse_hex_number("ff0000"))
    embed.add_field(name="Message Content:", value=f"```{message.content}```")
    embed.set_author(
        name=f"{message.author} ({message.author.id})", icon_url=message.author.avatar)
    channel = bot.get_channel(int(getSetting(os.getenv("SETTINGS_messageLog"))))
    await channel.send(embed=embed)   # type: ignore
