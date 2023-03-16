import logging
import time
import os
import sys
import discord
import requests
import datetime
from discord.ext import commands
import dotenv
from discord_webhook_logging import DiscordWebhookHandler
from modules.config.getConfig import settings as unsettings
settings = unsettings()
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


# Testing if webhook is valid, and announcing that the bot is booting
startupPost = requests.post(settings.getBotSetting("webhook-Url"), json={'content':f"KaspBot is Booting!\nTime (UTC): {datetime.datetime.utcnow()}"})
startupPost.raise_for_status()

time.sleep(1)



logging.basicConfig(filename='./logs/log.log', encoding='utf-8', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)-8s %(message)s')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
discordHandler = DiscordWebhookHandler(webhook_url=settings.getBotSetting("webhook-Url"),auto_flush=True)
discordHandler.setLevel(logging.INFO)

logger = logging.getLogger()
logger.addHandler(stream_handler)
logger.addHandler(discordHandler)

class KaspBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=";",
            intents=discord.Intents.all(),
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
        print(f"logging in with: {token}")
        bot.run(token=token, reconnect=True)
    else:
        sys.exit("Bad Bot Token in Database")