import time
import discord
from modules.logging.debugLog import debugLog
from modules.config.loadConfigs import botConfig

async def adminCommandLogs(user, command, channelId, bot):
    debugLog("admin command Logs was ran")
    embed = discord.Embed(title="A Command was ran")
    embed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar)
    embed.add_field(name="Command:", value=command, inline=False)
    embed.add_field(
        name="When:", value=f"<t:{int(time.time())}:T>", inline=False)
    embed.add_field(name="Where:", value=f"<#{channelId}>", inline=False)
    channel = bot.get_channel(int(botConfig()["admin_log_channel"]))
    await channel.send(embed=embed)     # type: ignore