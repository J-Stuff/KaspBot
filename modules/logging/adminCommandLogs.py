import sys
import datetime
import discord
import os
import logging
from discord.ext import commands
from discord.utils import format_dt
from config.getSetting import getSetting

async def adminCommandLogs(user:discord.User|discord.Member, message:str, channel, bot:commands.Bot):
    logging.info("Admin logging was fired")
    now = datetime.datetime.now()
    longDate = format_dt(now, "D")
    longTime = format_dt(now, "T")
    embed = discord.Embed(color=discord.colour.parse_hex_number("5151fa"), title="Admin logging")
    embed.set_author(name=user.name, icon_url=user.avatar.url) #type:ignore
    embed.add_field(name="Time", value=f"{longDate} @ {longTime}")
    embed.add_field(name="Channel", value=channel.mention)
    embed.add_field(name="Message", value=message)
    logChannelID = getSetting(os.getenv("SETTINGS_adminLog"))
    logChannel = await bot.fetch_channel(int(logChannelID))
    if not type(logChannel) == discord.TextChannel:
        sys.exit("BAD CHANNEL ID FOR: admin_log_channel")
    await logChannel.send(embed=embed) #type:ignore