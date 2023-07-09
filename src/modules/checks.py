import discord
from discord.ext import commands
from discord import app_commands
from _kaspBot import KaspBot

bot = KaspBot()

@staticmethod
def is_main_guild(interaction:discord.Interaction):
    return interaction.guild.id == bot.EnumGulds.MAIN #type:ignore


@staticmethod
def is_dev_guild(interaction:discord.Interaction):
    return interaction.guild.id == bot.EnumGulds.DEV #type:ignore


@staticmethod
def is_dm(interaction:discord.Interaction):
    return interaction.guild is None

@staticmethod
def is_main_guild_or_dev_guild(interaction:discord.Interaction):
    return interaction.guild.id in [bot.EnumGulds.MAIN, bot.EnumGulds.DEV] #type:ignore




@is_main_guild.error
async def is_main_guild_error(interaction:discord.Interaction, error:app_commands.AppCommandError):
    if isinstance(error, commands.CheckFailure):
        await interaction.response.send_message('This command can only be used in the main guild', ephemeral=True)
    else:
        raise error
    

@is_dev_guild.error
async def is_dev_guild_error(interaction:discord.Interaction, error:app_commands.AppCommandError):
    if isinstance(error, commands.CheckFailure):
        await interaction.response.send_message('This command can only be used in the dev guild', ephemeral=True)
    else:
        raise error
    

@is_dm.error
async def is_dm_error(interaction:discord.Interaction, error:app_commands.AppCommandError):
    if isinstance(error, commands.CheckFailure):
        await interaction.response.send_message('This command can only be used in a DM', ephemeral=True)
    else:
        raise error
    
@is_main_guild_or_dev_guild.error
async def is_main_guild_or_dev_guild_error(interaction:discord.Interaction, error:app_commands.AppCommandError):
    if isinstance(error, commands.CheckFailure):
        await interaction.response.send_message('This command can only be used in the main guild or the dev guild', ephemeral=True)
    else:
        raise error
