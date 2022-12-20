import json
import logging
import os
import random
import sys
import time
import typing

import discord
import requests
from discord.ext import commands, tasks

# -----

from modules.config.loadConfigs import botConfig, botJson

from modules.fun.statusRotate import funStatus

from modules.logging.adminCommandLogs import adminCommandLogs

from modules.messageLogger.onMessageEdit import onMessageEdit
from modules.messageLogger.onMessageDelete import onMessageDelete
from modules.messageFilter.messageFilter import msgCheck, doAddFilter, rmvFilter
from modules.logging.debugLog import debugLog

from modules.utilities.reactionRolesClasses import SpeciesRoles, ColorRoles, SORoles
from modules.utilities.modTickets import ModTicket, closeTicket
from modules.utilities.adminTools.verification import unv_scan, user_verf
from modules.utilities.adminTools.chatPurge import chatPurge
from modules.utilities.mutes.channelMutes import channelMute, channelUnMute
from modules.logging.userActions import onJoin, onLeaveRaw

# -----


if os.path.exists('./client_previous.log'):
    os.remove('./client_previous.log')

if os.path.exists('./client.log'):
    os.rename('./client.log', './client_previous.log')

handler = logging.FileHandler(
    filename='./client.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=';', intents=intents)
tree = bot.tree
guild = int(botConfig()["guild"])


# ===================================

@bot.event
async def on_message_delete(message):
    await onMessageDelete(message, bot)


@bot.event
async def on_message_edit(message_before, message_after):
    await onMessageEdit(message_before, message_after, bot)


@bot.event
async def on_message(message):
    await msgCheck(message, bot)
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    await onJoin(member, bot)

@bot.event
async def on_raw_member_remove(payload):
    await onLeaveRaw(payload, bot)

       

# ==================================


@tasks.loop(minutes=5)
async def do_funStatus():
    await funStatus(bot)


# =================================


@bot.command()
async def restart(ctx):
    debugLog("running command restart")
    if ctx.author.guild_permissions.manage_guild:
        await ctx.send("<a:loader2:1041678096228691980> Packing up and restarting... See you soon!")
        with open('./temp/reboot.bin', 'w') as fp:
            fp.write(str(ctx.channel.id))
        time.sleep(random.randint(10, 30))
        os.execv(f"{sys.executable}", ['python'] + sys.argv)


@bot.command()
async def status(ctx):
    debugLog("running command status")
    if ctx.author.guild_permissions.manage_messages:
        ping_ms = int(bot.latency * 1000)
        discord_api = requests.get(
            "https://discordstatus.com/api/v2/summary.json")
        dApiData = json.loads(discord_api.text)
        dApiStatus = dApiData["components"][1]["status"]
        if dApiStatus == "operational":
            operationalMessage = "<:green_heart:1034024591791771648> `Discord API Online`"
        else:
            operationalMessage = "<:broken_heart:1034024591791771648> `Discord API Degraded`"

        with open('./config/botInfo.json', 'r') as fp:
            info = json.loads(fp.read())
        await ctx.send(f"Pong!\n<:satellite:1034018740897075231><:stopwatch:1034018740897075231> `{str(ping_ms)} ms` **|** {operationalMessage}\nI last booted on <t:{uptimeunix}:F> (Which was <t:{uptimeunix}:R>)\nI'm running KaspBot Version: {info['version']}")


@bot.command()
async def refreshTree(ctx):
    debugLog("running command refreshTree")
    if ctx.author.guild_permissions.manage_guild:
        loader = await ctx.send("<a:loader:1039118414213554239> working on it...\n*This can take up to 110 seconds*")
        await tree.sync(guild=discord.Object(id=guild))
        time.sleep(5)
        await adminCommandLogs(ctx.author, f"`refreshTree`", ctx.channel.id, bot)
        await loader.delete()
        await ctx.send("Done!")


@bot.command()
async def sendSOembed(ctx):
    debugLog("running command sendSOembed")
    if ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a role based on your sexual orientation",
                              color=discord.colour.parse_hex_number("00a83d"))
        embed.add_field(name="Possible Options:", inline=False, value="<:hetro_flag:1038705337865342976> > Straight\n<:queer_flag:1038707440692232292> > Gay\n<:lesbian_flag:1038705904402583612> > Lesbian\n<:bisexual_flag:1038706509833588826> > Bisexual\n<:pansexual_flag:1038706723529162782> > Pansexual\n<:asexual_flag:1038706919231205406> > Asexual")
        await ctx.send(embed=embed, view=SORoles(bot))
        await adminCommandLogs(ctx.author, f"`sendSOembed`", ctx.channel.id, bot)


@bot.command()
async def sendCOLORembed(ctx):
    debugLog("running command sendCOLORembed")
    if ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a color role!",
                              color=discord.colour.parse_hex_number("00a83d"))
        embed.add_field(name="Please note", inline=False, value="If you select multiple options, the highest color in the order of the list will override ones below it (EG: Red will override any other choice | If you select Green & Purple, Green will override the color choice)")
        await ctx.send(embed=embed, view=ColorRoles(bot))
        await adminCommandLogs(ctx.author, f"`sendCOLORembed`", ctx.channel.id, bot)


@bot.command()
async def sendSPCembed(ctx):
    debugLog("running command sendSPCembed")
    if ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a Species role!",
                              color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed, view=SpeciesRoles(bot))
        await adminCommandLogs(ctx.author, f"`sendSPCembed`", ctx.channel.id, bot)


@bot.command()
async def sendReportEmbed(ctx):
    debugLog("running command sendSPCembed")
    if ctx.author.guild_permissions.manage_guild:
        embed = discord.Embed(title="Create a Ticket with the Moderators", description="Use the button below to create a ticket to contact our moderators!",
                              color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed, view=ModTicket(bot))
        await adminCommandLogs(ctx.author, f"`sendReportEmbed`", ctx.channel.id, bot)


@bot.command()
async def giveBlacklist(ctx):
    debugLog("running command giveBlacklist")
    if ctx.author.guild_permissions.manage_guild:
        await ctx.author.send(file=discord.File('./modules/messageFilter/blacklist.database.bin'))
        await ctx.send("Done! Check your DM's")


# ===================================================================================================================


@tree.command(name="channel-mute", description="Allow a moderator to channel mute a member", guild=discord.Object(id=guild))
async def dochannelMute(interaction, user: discord.Member, reason: str):
    await channelMute(interaction, user, reason, bot)


@tree.command(name="channel-unmute", description="Allow a moderator to channel un-mute a member", guild=discord.Object(id=guild))
async def dochannelUnMute(interaction, user: discord.Member):
    await channelUnMute(interaction, user, bot)


@tree.command(name="purge", description="Allows an admin to purge the chat", guild=discord.Object(id=guild))
async def purgeChat(interaction, count: int):
    await chatPurge(interaction, count, bot)


@tree.command(name="verify", description="Verify a user!", guild=discord.Object(id=guild))
async def verifyUser(interaction, target: discord.Member):
    await user_verf(interaction, target, bot)


@tree.command(name="unverified-scan", description="Scan the server for unverified users.", guild=discord.Object(id=guild))
async def unvScan(interaction):
    await unv_scan(interaction, bot)



@tree.command(name='ticket-close', description="Close a ticket", guild=discord.Object(id=guild))
async def do_CloseTicket(interaction, ticket: discord.TextChannel):
    await closeTicket(interaction, ticket, bot)


@tree.command(name='add-filter', description="Add a word to the filter", guild=discord.Object(id=guild))
async def do_addFilter(interaction, string: str):
    await doAddFilter(string, bot, interaction)


@tree.command(name='remove-filter', description="Remove a word from the filter", guild=discord.Object(id=guild))
async def do_removeFilter(interaction, string: str):
    await rmvFilter(string, bot, interaction)


@bot.event
async def on_ready():
    global uptimeunix
    os.system('cls')
    print("Starting up...")

    bot.add_view(SORoles(bot))
    bot.add_view(ColorRoles(bot))
    bot.add_view(SpeciesRoles(bot))
    bot.add_view(ModTicket(bot))
    bot.remove_command('help')
    do_funStatus.start()
    uptimeunix = int(time.time())

    if os.path.exists('./temp/reboot.bin'):
        with open('./temp/reboot.bin', 'r') as fp:
            announceChannelId = int(fp.read())
        announceChannel = bot.get_channel(announceChannelId)
        await announceChannel.send("Reboot successful!")  # type:ignore
        os.remove('./temp/reboot.bin')

    print("Ready!")


bot.run(botJson()["token"], log_handler=handler,
        log_level=logging.ERROR)  # type:ignore
# BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER-BUFFER
