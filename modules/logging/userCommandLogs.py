import discord
import datetime
from discord.ext import commands
from discord.utils import format_dt
import os
import logging
from config.getConfig import settings as unsettings
settings = unsettings()

async def userCommandLogs(user:discord.User|discord.Member, message:str, channel, bot:commands.Bot):
    logging.info("Admin logging was fired")
    now = datetime.datetime.now()
    longDate = format_dt(now, "D")
    longTime = format_dt(now, "T")
    embed = discord.Embed(color=discord.colour.parse_hex_number("5151fa"), title="User Logging")
    embed.set_author(name=user.name, icon_url=user.display_avatar.url) #type:ignore
    embed.add_field(name="Time", value=f"{longDate} @ {longTime}")
    embed.add_field(name="Channel", value=channel.mention)
    embed.add_field(name="Message", value=message)
    logChannel = await bot.fetch_channel(int(settings.getChannelID("commandLogs")))
    await logChannel.send(embed=embed)     # type: ignore