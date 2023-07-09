import discord
from discord.ext import commands
from discord.utils import format_dt
from _kaspBot import KaspBot
from discord import app_commands
from modules.checks import is_main_guild

class aboutCommand(commands.Cog):
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="about", description="About the bot")
    @app_commands.guild_only()
    @app_commands.check(is_main_guild)
    async def about(self, interaction:discord.Interaction):
        embed = discord.Embed(title="About", description="KaspBot", color=discord.Color.dark_teal())
        embed.add_field(name="Version", value=self.bot.info.VERSION, inline=False)
        embed.add_field(name="Author", value=self.bot.info.AUTHOR, inline=False)
        embed.add_field(name="Source", value=self.bot.info.SOURCE, inline=False)
        embed.add_field(name="Uptime", value=f"{format_dt(self.bot.uptime, 'F')} ({format_dt(self.bot.uptime, 'R')})", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

        
async def setup(bot:KaspBot):
    await bot.add_cog(aboutCommand(bot))