from discord.ext import commands
import discord
import os
from discord import app_commands
from config.getConfig import settings as preSettings
from modules.logging.userCommandLogs import userCommandLogs
from modules.logging.adminCommandLogs import adminCommandLogs
import logging
import random
settings = preSettings()


class adminSlash(commands.Cog, name="Admin Slash Commands"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Allows an admin to purge the chat")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purgeChat(self, interaction:discord.Interaction, count: int):
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
        await adminCommandLogs(interaction.user, f"Purged {count} messages!", interaction.channel, self.bot)

    @app_commands.command(name="verify", description="Verify a user!")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifyUser(self, interaction, target: discord.Member):
        from modules.utilities.verification import user_verf
        await user_verf(interaction, target, self.bot)

    @app_commands.command(name="unverified-scan", description="Scan and update the User Registry")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def unvScan(self, interaction):
        from modules.utilities.verification import unv_scan
        await unv_scan(interaction, self.bot)

    @app_commands.command(name='ticket-close', description="Close a ticket")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def do_CloseTicket(self, interaction, ticket: discord.TextChannel):
        from modules.utilities.modTickets import closeTicket
        await closeTicket(interaction, ticket, self.bot)

    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def do_warn(self, interaction:discord.Interaction, user:discord.Member, reason:str):
        from modules.utilities.warn import warn
        await warn(interaction, user, reason, self.bot)

    @app_commands.command(name="unverified-kick", description="Run the kick operation for unverified users")
    @app_commands.checks.has_permissions(administrator=True)
    async def do_unverifiedKick(self, interaction:discord.Interaction):
        from modules.utilities.verification import unverifiedKick
        await unverifiedKick(interaction, self.bot)

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError
    ):
        from modules.botMaintenance.appCommand_Errors import appCommand_Error
        await appCommand_Error(interaction, error, self.bot)

class userSlash(commands.Cog, name="User Slash Commands"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="boop", description="Boop a user")
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def userBoop(self, interaction:discord.Interaction, user:discord.Member|discord.User):
        with open('./database/boops.db', 'r') as fp:
            boopList = fp.read().splitlines()
            boop = random.choice(boopList)
            await userCommandLogs(interaction.user, f"/boop on {user.mention}", interaction.channel, self.bot)
            await interaction.response.send_message(f"{interaction.user.mention} *boops* {user.mention}")
            await interaction.channel.send(boop) #type:ignore


    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError
    ):
        from modules.botMaintenance.appCommand_Errors import appCommand_Error
        await appCommand_Error(interaction, error, self.bot)



async def setup(bot: commands.Bot):
    logging.info(f"{__file__} - Setting up...")
    guildID = int(settings.getMiscId("guildID"))
    await bot.add_cog(
        adminSlash(bot),
        guild=discord.Object(int(guildID))
    )
    await bot.add_cog(
        userSlash(bot),
        guild=discord.Object(int(guildID))
    )
    logging.info("Syncing tree...")
    sync = await bot.tree.sync()
    logging.info(str(sync))
    logging.info("Sync of tree complete!")
    logging.info(f"{__file__} - Done!")
