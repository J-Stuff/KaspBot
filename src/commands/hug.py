import os, discord, random
from discord.ext import commands
from _kaspBot import KaspBot
from discord import app_commands

class Hug(commands.Cog):
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        super().__init__()

    
    @app_commands.command(name="hug", description="Hug someone")
    @app_commands.guild_only()
    async def hug(self, interaction:discord.Interaction, user:discord.User):
        selectedHug = random.choice(os.listdir("./src/assets/hugs"))
        if interaction.user == user:
            await interaction.response.send_message(f"{interaction.user.mention} *hugs* themselves", ephemeral=False, file=discord.File(f"./src/assets/hugs/{selectedHug}"))
            return
        await interaction.response.send_message(f"{interaction.user.mention} *hugs* {user.mention}", ephemeral=False, file=discord.File(f"./src/assets/hugs/{selectedHug}"))


async def setup(bot:KaspBot):
    await bot.add_cog(Hug(bot))