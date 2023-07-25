import discord
from discord.ext import commands
from _kaspBot import KaspBot
from discord import app_commands
from src.modules.cogs import restart_all_cogs



class BotControl(commands.Cog):
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        super().__init__()


    @commands.command(name="logs")
    @commands.is_owner()
    async def logs(self, ctx:commands.Context):
        logFile = "./logs/kaspBot.log"
        oldLog = "./logs/kaspBot.log.old"
        await ctx.author.send(files=[discord.File(logFile), discord.File(oldLog)])
        await ctx.message.add_reaction("✅")


    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx:commands.Context):
        response = await ctx.reply(":loader:1128496479414259722: Reloading cogs...")
        await restart_all_cogs(self.bot)
        await response.edit(content=":white_check_mark: Reloaded cogs")
