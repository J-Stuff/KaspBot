from modules.fun.statusRotate import funStatus
import logging
from discord.ext import commands, tasks


class Loop(commands.Cog, name="Loop cogs"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.do_funStatus.start()


    @tasks.loop(minutes=2)
    async def do_funStatus(self):
        await funStatus(self.bot)

    @do_funStatus.before_loop
    async def beforeLogin(self):
        logging.info("Waiting for websocket")
        await self.bot.wait_until_ready()


async def setup(bot:commands.Bot):
    logging.info(f"{__file__} - Setting up...")
    await bot.add_cog(
        Loop(bot)
    )
    logging.info(f"{__file__} - Done!")