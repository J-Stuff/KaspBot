import discord
import discord.ext
from discord.ext import commands
from modules.config.loadConfigs import botConfig

async def userEventLog(embed: discord.Embed, bot: commands.Bot):
    logChannelId = botConfig()["message_log_channel"]
    logChannel = bot.get_channel(logChannelId)
    await logChannel.send(embed=embed) #type:ignore