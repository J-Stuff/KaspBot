import time
import discord
from modules.logging.debugLog import debugLog
from modules.config.loadConfigs import botConfig


async def adminCommandLogsMessage(user, message, bot):
    debugLog("Admin Command Log Message was ran!")
    embed = discord.Embed(title="Bot Message:")
    embed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar)
    embed.add_field(name="Message:", value=message, inline=False)
    embed.add_field(
        name="When:", value=f"<t:{int(time.time())}:T>", inline=False)
    channel = bot.get_channel(int(botConfig()["admin_log_channel"]))
    await channel.send(embed=embed)     # type: ignore