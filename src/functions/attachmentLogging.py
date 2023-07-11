import discord, random, os
from discord.ext import commands
from _kaspBot import KaspBot




class AttachmentLogging(commands.Cog):
    def __init__(self, bot:KaspBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        if not message.guild: return
        if message.guild.id != self.bot.EnumGulds.MAIN: return
        if message.attachments:
            for attachment in message.attachments:
                if message.guild.filesize_limit > attachment.size: continue
                tempLocation = f"temp/{random.randint(1, 100)}.tmp"
                with open(tempLocation, "wb") as f:
                    await attachment.save(f)
                channel = self.bot.get_channel(self.bot.EnumMainGuild.CHANNELS.value.ATTACHMENT_LOGS)
                backup = self.bot.get_channel(self.bot.EnumDevGuild.CHANNELS.value.BACKUP_LOGS)
                if type(channel) != discord.TextChannel: return
                if type(backup) != discord.TextChannel: return                    
                embed = discord.Embed(color=discord.Color.green(), timestamp=message.created_at, title="Attachment")
                embed.set_author(name=message.author, icon_url=message.author.display_avatar)
                embed.add_field(name="Message", value=message.content, inline=False)
                embed.add_field(name="Attachment", value=attachment.filename, inline=False)
                embed.add_field(name="Channel", value=message.channel.mention, inline=False) #type:ignore
                try:
                    await channel.send(embed=embed, file=discord.File(tempLocation))
                except:
                    pass
                os.remove(tempLocation)