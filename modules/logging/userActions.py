import discord
from discord.ext import commands
import time
from modules.logging.userEventLog import userEventLog
from modules.config.loadConfigs import botConfig


async def onJoin(member: discord.Member, bot: commands.Bot):
    guild = bot.get_guild(botConfig()["guild"])
    unv_role = guild.get_role(botConfig()["unverifiedRoleId"])  # type:ignore
    await member.add_roles(unv_role)  # type:ignore

    userJoinedEmbed = discord.Embed(
        title="User Joined!", color=discord.colour.parse_hex_number("45be00"))
    userJoinedEmbed.set_author(
        name=f"{member} ({member.id})", url=member.avatar)
    userJoinedEmbed.add_field(
        name="Username:", value=f"```{member}```", inline=False)
    userJoinedEmbed.add_field(
        name="User ID:", value=f"```{member.id}```", inline=False)
    userJoinedEmbed.add_field(
        name="Account Created", value=f"<t:{int(time.mktime(member.created_at.timetuple()))}:F>\n(Which was: <t:{int(time.mktime(member.created_at.timetuple()))}:R>)", inline=False)
    await userEventLog(userJoinedEmbed, bot)


async def onLeaveRaw(member: discord.RawMemberRemoveEvent, bot: commands.Bot):
    user = member.user
    userLeftEmbed = discord.Embed(
        title="User left!", colour=discord.colour.parse_hex_number("be0000"))
    userLeftEmbed.set_author(name=f"{user} ({user.id})", url=user.avatar)
    userLeftEmbed.add_field(
        name="Username:", value=f"```{user}```", inline=False)
    userLeftEmbed.add_field(
        name="User ID:", value=f"```{user.id}```", inline=False)
    userLeftEmbed.add_field(
        name="Account Created", value=f"<t:{int(time.mktime(user.created_at.timetuple()))}:F>\n(Which was: <t:{int(time.mktime(user.created_at.timetuple()))}:R>)", inline=False)
    await userEventLog(userLeftEmbed, bot)
