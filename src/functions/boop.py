import discord, os, random, logging
from discord.ext import commands
from discord import app_commands
from _kaspBot import KaspBot
from src.modules.checks import is_main_guild

class Boop(commands.Cog):
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        super().__init__()


    @app_commands.command(name="boop", description="Boop someone")
    @app_commands.check(is_main_guild)
    async def boop(self, interaction:discord.Interaction, user:discord.User):
        logging.info(f"{interaction.user} booped {user}")
        selectedBoop = random.choice(os.listdir("./src/assets/boops"))
        await interaction.response.send_message(f"{interaction.user.mention} *boops* {user.mention}", ephemeral=False, file=discord.File(f"./src/assets/boops/{selectedBoop}"))


async def setup(bot:KaspBot):
    await bot.add_cog(Boop(bot))