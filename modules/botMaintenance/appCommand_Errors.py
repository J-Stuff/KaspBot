import discord
from discord.ext import commands
import logging

async def TransformerError(interaction:discord.Interaction):
    await interaction.response.send_message("I cannot find that user anymore. They probably left the server.", ephemeral=True)
    logging.info("Sent TransformerError notice")


async def appCommand_Error(interaction:discord.Interaction, error:discord.app_commands.AppCommandError):
    logging.warning(error)
    if type(error) == discord.app_commands.errors.TransformerError:
        await TransformerError(interaction)