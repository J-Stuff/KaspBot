import discord, logging
from discord.ext import commands
from _kaspBot import KaspBot
from discord import app_commands





async def restart_all_cogs(bot:KaspBot):
    logging.info('Reloading cogs')
    for cog in bot.CogList:
        logging.info(f'Reloading {cog}')
        await bot.reload_extension(cog)
        logging.info(f'Reloaded {cog}')
    logging.info('Reloaded cogs')