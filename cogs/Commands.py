from discord.ext import commands
import discord
import os
from discord import app_commands
from config.getSetting import getSetting
import logging


class Slash(commands.Cog, name="Slash Commands"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Allows an admin to purge the chat")
    async def purgeChat(self, interaction, count: int):
        from modules.utilities.chatPurge import chatPurge
        await chatPurge(interaction, count, self.bot)

    @app_commands.command(name="verify", description="Verify a user!")
    async def verifyUser(self, interaction, target: discord.Member):
        from modules.utilities.verification import user_verf
        await user_verf(interaction, target, self.bot)

    @app_commands.command(name="unverified-scan", description="Scan and update the User Registry")
    async def unvScan(self, interaction):
        from modules.utilities.verification import unv_scan
        await unv_scan(interaction, self.bot)

    @app_commands.command(name='ticket-close', description="Close a ticket")
    async def do_CloseTicket(self, interaction, ticket: discord.TextChannel):
        from modules.utilities.modTickets import closeTicket
        await closeTicket(interaction, ticket, self.bot)

    @app_commands.command(name="warn", description="Warn a user")
    async def do_warn(self, interaction:discord.Interaction, user:discord.Member, reason:str):
        from modules.utilities.warn import warn
        await warn(interaction, user, reason, self.bot)

    @app_commands.command(name="unverified-kick", description="Run the kick operation for unverified users")
    async def do_unverifiedKick(self, interaction:discord.Interaction):
        from modules.utilities.verification import unverifiedKick
        await unverifiedKick(interaction, self.bot)

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError
    ):
        from modules.botMaintenance.appCommand_Errors import appCommand_Error
        await appCommand_Error(interaction, error)

async def setup(bot: commands.Bot):
    logging.info(f"{__file__} - Setting up...")
    guildID = int(getSetting(os.getenv("SETTINGS_guildID")))
    await bot.add_cog(
        Slash(bot),
        guild=discord.Object(int(guildID))
    )
    logging.info("Syncing tree...")
    sync = await bot.tree.sync(guild=discord.Object(id=int(getSetting(os.getenv("SETTINGS_guildID")))))
    logging.info(str(sync))
    logging.info("Sync of tree complete!")
    logging.info(f"{__file__} - Done!")
