import sys
import datetime
import discord
import os
import logging
logger = logging.getLogger('kaspbot')
from discord.ext import commands
from discord.utils import format_dt
from modules.config.getConfig import settings as unsetSettings
settings = unsetSettings()

async def adminCommandLogs(user:discord.User|discord.Member, message:str, channel, bot:commands.Bot):
    logger.info("Admin logging was fired")
    now = datetime.datetime.now()
    longDate = format_dt(now, "D")
    longTime = format_dt(now, "T")
    embed = discord.Embed(color=discord.colour.parse_hex_number("5151fa"), title="Admin logging")
    embed.set_author(name=user.name, icon_url=user.display_avatar.url) #type:ignore
    embed.add_field(name="Time", value=f"{longDate} @ {longTime}")
    embed.add_field(name="Channel", value=channel.mention)
    embed.add_field(name="Message", value=message)
    logChannelID = settings.getChannelID("adminLogs")
    logChannel = await bot.fetch_channel(int(logChannelID))
    if type(logChannel) is not discord.TextChannel:
        sys.exit("BAD CHANNEL ID FOR: admin_log_channel")
    await logChannel.send(embed=embed)