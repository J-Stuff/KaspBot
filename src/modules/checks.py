import discord
from discord.ext import commands
from discord import app_commands
from _kaspBot import KaspBot

bot = KaspBot()

@staticmethod
def is_main_guild(interaction:discord.Interaction):
    return interaction.guild.id == bot.EnumGulds.MAIN #type:ignore






@is_main_guild.error
async def is_main_guild_error(interaction:discord.Interaction, error:app_commands.AppCommandError):
    if isinstance(error, commands.CheckFailure):
        await interaction.response.send_message('This command can only be used in the main guild', ephemeral=True)
    else:
        raise error
