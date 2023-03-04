from discord.ext import commands
import time
import discord
import logging
from tinydb import TinyDB, Query
from config.getConfig import settings as unsettings
settings = unsettings()

class Listeners(commands.Cog, name="On Event Listeners"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    async def checkIfPinged(self, message:discord.Message):
        if self.bot.user.mentioned_in(message) and message.author != self.bot.user: #type:ignore
            if message.reference is None:
                if "@everyone" not in message.content and "@here" not in message.content:
                    await message.reply(f"Greetings {message.author.mention}!")

    @commands.Cog.listener()
    async def on_message_delete(self, message:discord.Message):
        logging.info(f"Message Deleted: {message.content}")
        botUser = self.bot.user
        if not botUser:
            return
        if message.author.id == botUser.id or message.content == None:
            return
        if type(message.channel) == discord.DMChannel:
            return
        unix = int(time.time())
        embed = discord.Embed(title="A message was Deleted!",
                            description=f"Deleted in: <#{message.channel.id}>\nAt <t:{unix}:T>", color=discord.colour.parse_hex_number("ff0000"))
        embed.add_field(name="Message Content:", value=f"```{message.content}```", inline=False)
        if message.attachments:
            targetChannel = message.channel
            if not targetChannel or type(targetChannel) is not discord.TextChannel:
                return
            if targetChannel.nsfw:
                embed.add_field(name="Contents Before:", value=f"```THIS CHANNEL IS NSFW. TO PROTECT UNDERAGE USERS, ATTACHMENTS HAVE BEEN REMOVED FROM THIS EMBED!```")
            else:
                embed.add_field(name="Attachments", value=message.attachments, inline=False)
        embed.set_author(
            name=f"{message.author} ({message.author.id})", icon_url=message.author.avatar)
        channel = self.bot.get_channel(int(settings.getChannelID("messageLogs")))
        if type(channel) is not discord.TextChannel:
            return
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before:discord.Message, message_after:discord.Message):
        botUser = self.bot.user
        if not botUser:
            return
        if message_before.author.id == botUser.id or message_after.content == message_before.content:
            return
        if type(message_before.channel) == discord.DMChannel:
            return
        unix = int(time.time())
        embed = discord.Embed(title="A message was Edited!",
                            description=f"Edited in: <#{message_before.channel.id}>\nAt <t:{unix}:T>", color=discord.colour.parse_hex_number("fff500"))
        embed.add_field(name="Message before:",
                        value=f"```{message_before.content}```", inline=False)
        embed.add_field(name="Message after:",
                        value=f"```{message_after.content}```", inline=False)
        if message_before.attachments or message_after.attachments:
            targetChannel = message_before.channel
            if not targetChannel or type(targetChannel) is not discord.TextChannel:
                return
            if targetChannel.nsfw:
                embed.add_field(name="Contents Before:", value=f"```THIS CHANNEL IS NSFW. TO PROTECT UNDERAGE USERS, ATTACHMENTS HAVE BEEN REMOVED FROM THIS EMBED!```")
                embed.add_field(name="Contents After:", value=f"```THIS CHANNEL IS NSFW. TO PROTECT UNDERAGE USERS, ATTACHMENTS HAVE BEEN REMOVED FROM THIS EMBED!```")
            else:
                embed.add_field(name="Contents Before:", value=f"```{message_before.attachments}```")
                embed.add_field(name="Contents After:", value=f"```{message_after.attachments}```")
        embed.set_author(name=f"{message_before.author} ({message_before.author.id})",
                        icon_url=message_before.author.avatar)
        channel = self.bot.get_channel(int(settings.getChannelID("messageLogs")))
        if type(channel) is not discord.TextChannel:
            return
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        await self.checkIfPinged(message)

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        logging.info("On join fired!")
        guild = member.guild
        unv_role = guild.get_role(int(settings.getMiscId("unverifiedID")))
        await member.add_roles(unv_role, reason="New user has joined the guild, Adding unverified role!")  # type:ignore

        userJoinedEmbed = discord.Embed(
            title="User Joined!", color=discord.colour.parse_hex_number("45be00"))
        userJoinedEmbed.set_author(
            name=f"{member} ({member.id})", icon_url=member.avatar)
        userJoinedEmbed.add_field(
            name="Username:", value=f"```{member}```", inline=False)
        userJoinedEmbed.add_field(
            name="User ID:", value=f"```{member.id}```", inline=False)
        userJoinedEmbed.add_field(
            name="Account Created", value=f"<t:{int(time.mktime(member.created_at.timetuple()))}:F>\n(Which was: <t:{int(time.mktime(member.created_at.timetuple()))}:R>)", inline=False)
        logChannel = await self.bot.fetch_channel(int(settings.getChannelID("accountLogs")))
        if type(logChannel) is not discord.TextChannel:
            return
        await logChannel.send(embed=userJoinedEmbed)

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload:discord.RawMemberRemoveEvent):
        logging.info("On left fired!")
        user = payload.user
        userLeftEmbed = discord.Embed(
            title="User left!", colour=discord.colour.parse_hex_number("be0000"))
        userLeftEmbed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar)
        userLeftEmbed.add_field(
            name="Username:", value=f"```{user}```", inline=False)
        userLeftEmbed.add_field(
            name="User ID:", value=f"```{user.id}```", inline=False)
        userLeftEmbed.add_field(
            name="Account Created", value=f"<t:{int(time.mktime(user.created_at.timetuple()))}:F>\n(Which was: <t:{int(time.mktime(user.created_at.timetuple()))}:R>)", inline=False)
        logChannel = await self.bot.fetch_channel(int(settings.getChannelID("accountLogs")))
        if type(logChannel) is not discord.TextChannel:
            return
        await logChannel.send(embed=userLeftEmbed)
        db = TinyDB('./database/verification.json')
        User = Query()
        result = db.remove(User.id == str(user.id))

    
    @commands.Cog.listener()
    async def on_ready(self):
        from modules.utilities.reactionRolesClasses import init as ReactionRolesInit
        from modules.utilities.modTickets import ModTicket
        from modules.utilities.verification import verificationClass
        logging.info("Starting up...")

        ReactionRolesInit(self.bot)
        self.bot.add_view(verificationClass(self.bot))
        self.bot.add_view(ModTicket(self.bot))

        from modules.utilities.verification import verificationNotify
        verificationNotify(self.bot) # INIT THE VERIFICATION NOTIFIER

        with open('./database/uptime.db', 'w') as fp:
            fp.write(str(time.time()))

        logging.info("Ready!")

async def setup(bot:commands.Bot):
    logging.info(f"{__file__} - Setting up...")
    await bot.add_cog(
        Listeners(bot)
    )
    logging.info(f"{__file__} - Done!")