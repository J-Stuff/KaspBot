import os
import time
import discord
import logging
from discord.ext import commands
from config.getSetting import getSetting
async def onMessageEdit(message_before:discord.Message, message_after:discord.Message, bot:commands.Bot):
    if message_before.author.id == bot.user.id or message_after.content == message_before.content:  # type: ignore
        return
    unix = int(time.time())
    embed = discord.Embed(title="A message was Edited!",
                          description=f"Edited in: <#{message_before.channel.id}>\nAt <t:{unix}:T>", color=discord.colour.parse_hex_number("fff500"))
    embed.add_field(name="Message before:",
                    value=f"```{message_before.content}```", inline=False)
    embed.add_field(name="Message after:",
                    value=f"```{message_after.content}```", inline=False)
    if message_before.attachments or message_after.attachments:
        embed.add_field(name="Contents Before:", value=f"```{message_before.attachments}```")
        embed.add_field(name="Contents After:", value=f"```{message_after.attachments}```")
    embed.set_author(name=f"{message_before.author} ({message_before.author.id})",
                     icon_url=message_before.author.avatar)
    channel = bot.get_channel(int(getSetting(os.getenv("SETTINGS_messageLog"))))
    await channel.send(embed=embed) #type:ignore
