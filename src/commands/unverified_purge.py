import discord, random, logging, asyncio
from discord.ext import commands
from discord import app_commands
from _kaspBot import KaspBot
from src.modules.checks import is_mod


class UnverifiedPurge(commands.Cog):
    async def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="unverified_purge")
    @app_commands.guild_only()
    @app_commands.check(is_mod)
    async def unv_purge(self, interaction:discord.Interaction):
        guild = interaction.guild
        if type(guild) != discord.Guild:
            await interaction.response.send_message("Something went wrong. Please try again.")
            return
        unverifiedRole = guild.get_role(self.bot.EnumMainGuild.ROLES.value.UNVERIFIED)
        if not unverifiedRole:
            await interaction.response.send_message("Something went wrong. Please try again.")
            return
        await interaction.response.defer()
        challenge = random.randint(100000, 999999)
        logging.info("Generated challenge: " + str(challenge))
        challengeEmbed = discord.Embed(title="Confirm unverified purge", description="Are you sure you want to purge all unverified users?", color=discord.Color.red())
        challengeEmbed.add_field(name="Challenge", value=str(challenge))
        challengeEmbed.add_field(name="Type this code within 20 seconds below to confirm", value="This is to prevent accidental purges.")
        challengeEmbed.set_footer(text="This action is irreversible.")
        await interaction.followup.send(embed=challengeEmbed)
        try:
            response = await self.bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel, timeout=20)
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond. Action cancelled.", ephemeral=True)
            return
        if response.content == str(challenge):
            await interaction.followup.send("Purging all unverified users...", ephemeral=True)
            await guild.prune_members(days=7, compute_prune_count=False, roles=[unverifiedRole], reason="Unverified purge")
            await interaction.followup.send("Successfully purged all unverified users.", ephemeral=True)
        else:
            await interaction.followup.send("Incorrect challenge code. Action cancelled.", ephemeral=True)
            return