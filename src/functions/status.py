import discord, logging, random
from discord.ext import commands, tasks
from discord.utils import format_dt
from _kaspBot import KaspBot


class Status(commands.Cog):
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        self.status_loop.start()
        super().__init__()


    @tasks.loop(seconds=60)
    async def status_loop(self):
        logging.info("Updating status")
        selectedStatus = random.choice(self.bot.statuses)
        await self.bot.change_presence(activity=selectedStatus, status=discord.Status.online) if not self.bot.info.DEVELOPMENT else await self.bot.change_presence(activity=discord.Activity(name="in Development Mode", type=discord.ActivityType.playing), status=discord.Status.idle)
        logging.info("Updated status")

    @status_loop.before_loop
    async def before_status_loop(self):
        await self.bot.wait_until_ready()
        logging.info("Status loop ready")


async def setup(bot:KaspBot):
    await bot.add_cog(Status(bot))