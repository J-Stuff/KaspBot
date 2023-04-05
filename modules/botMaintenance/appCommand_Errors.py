import discord
from discord.ext import commands
import logging
logger = logging.getLogger('kaspbot')
from modules.logging.adminCommandLogs import adminCommandLogs

async def TransformerError(interaction:discord.Interaction):
    await interaction.response.send_message("I cannot find that user anymore. They probably left the server.", ephemeral=True)
    logger.info("Sent TransformerError notice")

async def MissingPermissions(interaction:discord.Interaction, bot:commands.Bot):
    await interaction.response.send_message("You don't have permissions to run this command!", ephemeral=True)
    await adminCommandLogs(interaction.user, f"Tried to run {interaction.command.name} but failed due to lack of permissions", interaction.channel, bot) #type:ignore
    logger.info("Sent MissingPermissions notice")

async def CommandOnCooldown(interaction:discord.Interaction, bot:commands.Bot, cooldown:int):
    await interaction.response.send_message(f"This command is on cooldown!\nYou can run it again in {cooldown} seconds.", ephemeral=True)


async def appCommand_Error(interaction:discord.Interaction, error:discord.app_commands.AppCommandError, bot:commands.Bot):
    logger.warning(f"{interaction.user} // {error}")
    logger.debug(type(error))
    if isinstance(error, discord.app_commands.errors.TransformerError):
        await TransformerError(interaction)
    if isinstance(error, commands.MissingPermissions):
        await MissingPermissions(interaction, bot)
    if isinstance(error, discord.app_commands.errors.CommandOnCooldown):
        cooldown = int(error.retry_after)
        await CommandOnCooldown(interaction, bot, cooldown)
