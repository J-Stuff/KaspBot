import time
import discord
from modules.logging.debugLog import debugLog
from modules.config.loadConfigs import botConfig
from modules.messageFilter.filter import getWlChannels
whitelist = getWlChannels()

async def onMessageDelete(message, bot):
    debugLog(f"Message Deleted: {message.content}")
    if message.author.id == bot.user.id or message.content == None:  
        return
    try:
        if str(message.channel.category.id) in str(whitelist): 
            return
    except:
        pass

    author = message.author 
    author: discord.Member

    if author.guild_permissions.manage_messages:
        return
    unix = int(time.time())
    embed = discord.Embed(title="A message was Deleted!",
                          description=f"Deleted in: <#{message.channel.id}>\nAt <t:{unix}:T>", color=discord.colour.parse_hex_number("ff0000"))
    embed.add_field(name="Message Content:", value=f"```{message.content}```")
    embed.set_author(
        name=f"{message.author} ({message.author.id})", icon_url=message.author.avatar)
    channel = bot.get_channel(int(botConfig()["message_log_channel"]))
    await channel.send(embed=embed)   # type: ignore
