
import time
import discord
from modules.config.loadConfigs import botConfig
from modules.messageFilter.filter import getWlChannels
whitelist = getWlChannels()

async def onMessageEdit(message_before, message_after, bot):
    if message_before.author.id == bot.user.id or message_after.content == message_before.content:  # type: ignore
        return
    try:
        if str(message_before.channel.category.id) in str(whitelist): 
            return
    except:
        pass

    author = message_before.author 
    author: discord.Member

    if author.guild_permissions.manage_messages:
        return
    unix = int(time.time())
    embed = discord.Embed(title="A message was Edited!",
                          description=f"Edited in: <#{message_before.channel.id}>\nAt <t:{unix}:T>", color=discord.colour.parse_hex_number("fff500"))
    embed.add_field(name="Message before:",
                    value=f"```{message_before.content}```", inline=False)
    embed.add_field(name="Message after:",
                    value=f"```{message_after.content}```", inline=False)
    embed.set_footer(text=message_before.author,
                     icon_url=message_before.author.avatar)
    embed.set_author(name=f"{message_before.author} ({message_before.author.id})",
                     icon_url=message_before.author.avatar)
    channel = bot.get_channel(int(botConfig()["message_log_channel"]))
    await channel.send(embed=embed)   # type: ignore # type: ignore
