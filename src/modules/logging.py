import discord, logging, datetime
from _kaspBot import KaspBot




class Logger():
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot


    async def CustomUserLog(self, embed:discord.Embed):
        logging.info("Custom User logging was fired!")
        channel = await self.bot.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.USER_LOGS)
        backup = await self.bot.fetch_channel(self.bot.EnumDevGuild.CHANNELS.value.BACKUP_LOGS)
        if type(channel) != discord.TextChannel: return
        if type(backup) != discord.TextChannel: return
        await channel.send(embed=embed)
        await backup.send(embed=embed)


    async def MessageEdited(self, before:discord.Message, after:discord.Message):
        logging.info("Message edited logging was fired!")
        if before.author.bot or after.author.bot: logging.info("Logging aborted because the author was a bot!"); return
        if not before.guild or not after.guild: logging.info("Logging aborted because the message was sent in a DM!"); return
        if before.guild.id != self.bot.EnumGulds.MAIN or after.guild.id != self.bot.EnumGulds.MAIN: logging.info("Logging aborted because the message was sent in the dev guild!"); return
        if type(before.channel) != discord.TextChannel or type(after.channel) != discord.TextChannel: logging.info("Logging aborted because the message was sent in a non-text channel!"); return
        channel = await self.bot.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.USER_LOGS)
        backup = await self.bot.fetch_channel(self.bot.EnumDevGuild.CHANNELS.value.BACKUP_LOGS)
        if type(channel) != discord.TextChannel: return
        if type(backup) != discord.TextChannel: return
        embed = discord.Embed(
            title="Message Edited",
            color=discord.Color.yellow(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=before.author, icon_url=before.author.display_avatar)
        if before.content != None: embed.add_field(name="Before", value=before.content, inline=False)
        else: embed.add_field(name="Before", value="None", inline=False)
        if after.content != None: embed.add_field(name="After", value=after.content, inline=False)
        else: embed.add_field(name="After", value="None", inline=False)
        if before.attachments != None and not before.channel.nsfw: embed.add_field(name="Attachment(s) Before:", value=before.attachments, inline=True)
        elif before.attachments != None and before.channel.nsfw: embed.add_field(name="Attachment(s) Before:", value="`NSFW`", inline=True)
        if after.attachments != None and not after.channel.nsfw: embed.add_field(name="Attachment(s) After:", value=after.attachments, inline=True)
        elif after.attachments != None and after.channel.nsfw: embed.add_field(name="Attachment(s) After:", value="`NSFW`", inline=True)
        await channel.send(embed=embed)
        await backup.send(embed=embed)


    async def MessageDeleted(self, message:discord.Message):
        logging.info("Message deleted logging was fired!")
        if message.author.bot: logging.info("Logging aborted because the author was a bot!"); return
        if not message.guild: logging.info("Logging aborted because the message was sent in a DM!"); return
        if message.guild.id != self.bot.EnumGulds.MAIN: logging.info("Logging aborted because the message was sent in the dev guild!"); return
        if type(message.channel) != discord.TextChannel: logging.info("Logging aborted because the message was sent in a non-text channel!"); return
        channel = await self.bot.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.USER_LOGS)
        backup = await self.bot.fetch_channel(self.bot.EnumDevGuild.CHANNELS.value.BACKUP_LOGS)
        if type(channel) != discord.TextChannel: return
        if type(backup) != discord.TextChannel: return
        embed = discord.Embed(
            title="Message Deleted",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=message.author, icon_url=message.author.display_avatar)
        if message.content != None: embed.add_field(name="Message", value=message.content, inline=False)
        else: embed.add_field(name="Message", value="None", inline=False)
        if message.attachments != None and not message.channel.nsfw: embed.add_field(name="Attachment(s):", value=message.attachments, inline=True)
        elif message.attachments != None and message.channel.nsfw: embed.add_field(name="Attachment(s):", value="`NSFW`", inline=True)
        await channel.send(embed=embed)
        await backup.send(embed=embed)


    async def MemberJoined(self, member:discord.Member):
        logging.info("Member joined logging was fired!")
        channel = await self.bot.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.USER_LOGS)
        backup = await self.bot.fetch_channel(self.bot.EnumDevGuild.CHANNELS.value.BACKUP_LOGS)
        if type(channel) != discord.TextChannel: return
        if type(backup) != discord.TextChannel: return
        embed = discord.Embed(
            title="Member Joined",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=member, icon_url=member.display_avatar)
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)
        await backup.send(embed=embed)

    
    async def MemberLeft(self, member:discord.Member):
        logging.info("Member left logging was fired!")
        channel = await self.bot.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.USER_LOGS)
        backup = await self.bot.fetch_channel(self.bot.EnumDevGuild.CHANNELS.value.BACKUP_LOGS)
        if type(channel) != discord.TextChannel: return
        if type(backup) != discord.TextChannel: return
        embed = discord.Embed(
            title="Member Left",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=member, icon_url=member.display_avatar)
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)
        await backup.send(embed=embed)


    async def MemberBanned(self, user:discord.User):
        logging.info("Member banned logging was fired!")
        channel = await self.bot.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.USER_LOGS)
        backup = await self.bot.fetch_channel(self.bot.EnumDevGuild.CHANNELS.value.BACKUP_LOGS)
        if type(channel) != discord.TextChannel: return
        if type(backup) != discord.TextChannel: return
        embed = discord.Embed(
            title="Member Banned",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=user, icon_url=user.display_avatar)
        embed.set_footer(text=f"ID: {user.id}")
        await channel.send(embed=embed)
        await backup.send(embed=embed)


    async def AdminLogging(self, user:discord.User|discord.Member, actionLocation, action:str):
        logging.info("Admin logging was fired!")
        channel = await self.bot.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.ADMIN_LOGS)
        backup = await self.bot.fetch_channel(self.bot.EnumDevGuild.CHANNELS.value.BACKUP_LOGS)
        if type(channel) != discord.TextChannel: return
        if type(backup) != discord.TextChannel: return
        embed = discord.Embed(
            title="Admin Action",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=user, icon_url=user.display_avatar)
        embed.add_field(name="Action", value=action, inline=False)
        embed.add_field(name="Channel", value=actionLocation.mention, inline=False)
        await channel.send(embed=embed)
        await backup.send(embed=embed)