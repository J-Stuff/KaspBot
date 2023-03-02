import discord
import os
from discord.ext import commands
import time
import logging
from config.getConfig import settings as unsettings
settings = unsettings()


async def onJoin(member: discord.Member, bot: commands.Bot):
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
    logChannel = await bot.fetch_channel(int(settings.getChannelID("accountLogs")))
    await logChannel.send(embed=userJoinedEmbed) #type:ignore




async def onLeaveRaw(member: discord.RawMemberRemoveEvent, bot: commands.Bot):
    logging.info("On left fired!")
    user = member.user
    userLeftEmbed = discord.Embed(
        title="User left!", colour=discord.colour.parse_hex_number("be0000"))
    userLeftEmbed.set_author(name=f"{user} ({user.id})", icon_url=user.avatar)
    userLeftEmbed.add_field(
        name="Username:", value=f"```{user}```", inline=False)
    userLeftEmbed.add_field(
        name="User ID:", value=f"```{user.id}```", inline=False)
    userLeftEmbed.add_field(
        name="Account Created", value=f"<t:{int(time.mktime(user.created_at.timetuple()))}:F>\n(Which was: <t:{int(time.mktime(user.created_at.timetuple()))}:R>)", inline=False)
    logChannel = await bot.fetch_channel(int(settings.getChannelID("accountLogs")))
    await logChannel.send(embed=userLeftEmbed) #type:ignore
