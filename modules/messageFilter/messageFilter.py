from modules.messageFilter.filter import getFilter, getWlChannels, removeFilter, addFilter
from modules.config.loadConfigs import botConfig
from modules.logging.adminCommandLogsMessage import adminCommandLogsMessage
from modules.logging.debugLog import debugLog
import discord
import datetime
import re

async def doAddFilter(phrase, bot, interaction):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    addFilter(phrase)
    await adminCommandLogsMessage(interaction.user, f"ADMIN Added word/phrase to the filter: {phrase}", bot)
    await interaction.response.send_message(f"Done! Added the word '{phrase}' to the filter", ephemeral=True)


async def rmvFilter(phrase, bot, interaction):
    result = removeFilter(phrase)
    if not result:
        await interaction.response.send_message(f"The word or string '{phrase}' is not in the filter!", ephemeral=True)
    elif result:
        await adminCommandLogsMessage(interaction.user, f"Phrase '{phrase}' was **removed** from the global filter", bot)
        await interaction.response.send_message(f"The word or string '{phrase}' was removed from the global filter!", ephemeral=True)


async def msgCheck(message: discord.Message, bot):    
    debugLog("ON MESSAGE")
    blacklist = getFilter()
    whitelist = getWlChannels()

    try:
        if str(message.channel.category.id) in str(whitelist): #type:ignore
            return
    except:
        pass

    author = message.author #type:ignore
    author: discord.Member

    if author.guild_permissions.manage_messages:
        return
    
    msg_content = message.content
    msg_content = re.sub(" +", " ", msg_content)
    msg_content = msg_content.lower()
    
    for blacklistString in blacklist:
        for word in msg_content.split(' '):
            if blacklistString.lower() == word:
                await message.delete()
                await message.author.timeout(datetime.timedelta(minutes=5), reason=f"Auto Timeout > Triggered blacklist ({blacklistString})") #type:ignore
                await message.channel.send(f"Hey now.. That's a little TOO stinky to say here.. <@{message.author.id}>")
                embed = discord.Embed(title="The blacklist was triggered!!", color=discord.colour.parse_hex_number(
                    "ff0000"), timestamp=datetime.datetime.now(), description="The user was Timed out for 5 minutes!")
                embed.set_author(
                    name=f"{message.author} ({message.author.id})", icon_url=message.author.avatar)
                embed.add_field(name="Where:", value=f"<#{message.channel.id}>", inline=False)
                embed.add_field(name="Sentence:", value=f"||{message.content}||", inline=False)
                embed.add_field(name="Trigger:", value=f"||{blacklistString}||", inline=False)
                channel = bot.get_channel(int(botConfig()["message_log_channel"]))
                await channel.send(embed=embed)
