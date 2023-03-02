from modules.logging.adminCommandLogs import adminCommandLogs
import discord
from discord.ext import commands
import logging
async def chatPurge(interaction:discord.Interaction, count, bot:commands.Bot):
    channel = interaction.channel
    if not channel:
        logging.fatal("Channel is None in purge, Failing!")
        return
    if type(channel) is not discord.TextChannel:
        logging.info("Channel is not textchannel when purge called. Failing")
        return
    await interaction.response.defer(ephemeral=False, thinking=True)
    await channel.purge(limit=count)
    await channel.send(f"Done! Purged `{count}` messages!")
    await adminCommandLogs(interaction.user, f"Purged {count} messages!", interaction.channel, bot)