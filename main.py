import logging
import os
import sys
import discord
from discord.ext import commands
import dotenv
dotenv.load_dotenv('./.env')
try:
    os.remove('./logs/log.prev.log')
except:
    pass
try:
    os.rename('./logs/log.log', './logs/log.prev.log')
except:
    pass
open('./database/cogs.db', 'w').close()

if os.path.exists('./.env'):
    dotenv.load_dotenv('./.env')

logging.basicConfig(filename='./logs/log.log', encoding='utf-8', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)-8s %(message)s')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(stream_handler)

class KaspBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=";",
            intents=discord.Intents.all()
        )

    async def setup_hook(self):
        logging.info("Setup hook run!")
        from modules.botMaintenance.cog_controller import cogController
        controller = cogController(self)
        await controller.initCogs()
        logging.info("Cogs initialized!")

    async def on_ready(self):
        logging.info(f"Connected as {self.user}")


if __name__ in "__main__":
    bot = KaspBot()
    token = os.getenv("discord_token") 
    if token:
        logging.info(f"logging in with: {token}")
        bot.run(token=token, reconnect=True)
    else:
        sys.exit("Bad Bot Token in Database")