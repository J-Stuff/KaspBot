from discord.ext import commands
from modules.logging.adminCommandLogs import adminCommandLogs
from modules.config.getConfig import settings as unsettings
settings = unsettings()
import discord
import sys
import json
import requests
import random
import logging
logger = logging.getLogger('kaspbot')
import time
import datetime
import asyncio

class Admin(commands.Cog, name="Admin Commands"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.MissingPermissions):
            command = ctx.command
            if not command:
                return
            logger.info(f"[{ctx.author.id}] failed command [{command.name}] // noPerm [{error}]")
            await ctx.reply("You don't have permission to do that!")

    # =====================
    @commands.command(help="Shows the bot ping, version & status. Requires manage_messages", brief="Bot Status.")
    @commands.has_guild_permissions(manage_messages=True)
    async def status(self, ctx:commands.Context):
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Issued command")
        ping_ms = int(self.bot.latency * 1000)
        discord_api = requests.get(
            "https://discordstatus.com/api/v2/summary.json")
        discord_api.raise_for_status()
        dApiData = json.loads(discord_api.text)
        dApiStatus = dApiData["components"][0]["status"]
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Discord Status is: {dApiStatus}")
        if dApiStatus == "operational":
            operationalMessage = "<:green_heart:1034024591791771648> `Discord API Online`"
        else:
            operationalMessage = "<:broken_heart:1034024591791771648> `Discord API Degraded`"

        with open('./database/uptime.db', 'r') as fp:
            uptimeUnix = float(fp.read())
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-uptimeUnix))))
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Bot Uptime is: {uptime}")
        info = "1.2.2d (24.3.23)"
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Running version: {info}")
        await ctx.send(f"Pong!\n<:satellite:1034018740897075231> `{str(ping_ms)} ms`\n{operationalMessage}\nI'm running KaspBot Version: {info}\nUptime: {uptime}")
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Sent response!")

    @commands.command(help="Send the embed for reaction roles. Requires manage_guild", brief="Reaction Roles Embed")
    @commands.has_guild_permissions(manage_guild=True)
    async def sendRRembed(self, ctx: commands.Context):
        from modules.utilities.reactionRolesClasses import SORoles, SpeciesRoles, ColorRoles, GenderRoles, PronounRoles
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Issued command")
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Processing Reaction Buttons")
        embed0 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself an orientation role\n_                                                                                                                                                                                                                _",
                            color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed0, view=SORoles(self.bot))
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Processed SO Roles")

        embed1 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a pronoun role\n_                                                                                                                                                                                                                _",
                            color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed1, view=PronounRoles(self.bot))
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Processed Pronoun Roles")

        embed2 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a gender role\n_                                                                                                                                                                                                                _",
                            color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed2, view=GenderRoles(self.bot))
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Processed Gender Roles")

        embed3 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a color role\n_                                                                                                                                                                                                                _",
                            color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed3, view=ColorRoles(self.bot))
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Processed Colo(u)r Roles")

        embed4 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a species role\n_                                                                                                                                                                                                                _",
                            color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed4, view=SpeciesRoles(self.bot))
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Processed Species Roles")

        await adminCommandLogs(ctx.author, f"Sent the ReactionRoles Embeds", ctx.channel, self.bot)
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Sent Response!")
        

    @commands.command(help="Send the report embed. Requires: manage_guild", brief="Send Report Embed")
    @commands.has_guild_permissions(manage_guild=True)
    async def sendReportEmbed(self, ctx:commands.Context):
        from modules.utilities.modTickets import ModTicket
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Issued command")
        embed = discord.Embed(title="Create a Ticket with the Moderators", description="Use the button below to create a ticket to contact our moderators!",
                            color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed, view=ModTicket(self.bot))
        await adminCommandLogs(ctx.author, f"Sent the Report Embed", ctx.channel, self.bot)
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Sent Response!")

    @commands.command(help="Send the verification embed. Requires: manage_guild", brief="Send Verif Embed")
    @commands.has_guild_permissions(manage_guild=True)
    async def sendVerEmbed(self, ctx:commands.Context):
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Issued command")
        from modules.utilities.verification import verificationClass
        embed = discord.Embed(title="Begin Verification", description="Use the button below to begin Verification!",
                            color=discord.colour.parse_hex_number("00a83d"))
        await ctx.send(embed=embed, view=verificationClass(self.bot))
        await adminCommandLogs(ctx.author, f"Sent the Verification Embed", ctx.channel, self.bot)
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Sent Response")
        
    @commands.command(help="Reload the bot. Requires: administrator", brief="Reload")
    @commands.has_guild_permissions(administrator=True)
    async def reload(self, ctx:commands.Context):
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Issued Command")
        from modules.botMaintenance.cog_controller import cogController
        controller = cogController(self.bot)
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Initialized Controller")        
        await ctx.reply("<:arrows_counterclockwise:1077506380463870023> Reloading now...")
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Reloading cogs...")
        await controller.reloadCogs()
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Cogs Reload Success!")
        await ctx.send("Done!")
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Sent Response!")
        await adminCommandLogs(ctx.author, "Reloaded the bot", ctx.channel, self.bot)

    @commands.command(help="Echos what is said in the command. Requires: mention_everyone", brief="Echo message")
    @commands.has_guild_permissions(mention_everyone=True)
    async def echo(self, ctx:commands.Context, *, repeat:str):
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Issued Command > Content: {repeat}")
        await ctx.message.delete()
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Deleted User Message")
        await ctx.send(f"{repeat}")
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Echoed message")
        await adminCommandLogs(ctx.author, f"Made me echo: {repeat}", ctx.channel, self.bot)
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Done!")

    @commands.command(help="Sends a message in the specified channel. Requires: mention_everyone", breif="Send Message")
    @commands.has_guild_permissions(mention_everyone=True)
    async def send(self, ctx:commands.Context, channel:discord.TextChannel, *, message:str):
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Issued Command > Channel: {channel.name} > Content: {message}")
        await channel.send(message)
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Sent message")
        await adminCommandLogs(ctx.author, f"Made me send a message in {channel.mention}: {message} ", ctx.channel, self.bot)
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Done!")

    @commands.command(help="Shut down the bot. Requires: administrator", brief="Shutdown the Bot")
    @commands.has_guild_permissions(administrator=True)
    async def shutdown(self, ctx:commands.Context):
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Shutting down...")
        confirm = random.randint(111, 999)
        logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Confirm code is: {confirm}")
        confirmEmbed = discord.Embed(title="Warning!!!", 
                                    description=f"The action you are about to take is **Destructive**\n\nYou are about to shut me down...\n\nDo you understand that after starting this action, that it cannot be stopped until complete?\n\nType the following code within 20 seconds to confirm. Or wait for 20 seconds to cancel. \n`{confirm}`",
                                    color=discord.colour.parse_hex_number("ff0000"))
        await ctx.send(embed=confirmEmbed)
        def check(m:discord.Message):
            logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Testing to see if response matches challange code || Challenge code: {confirm} // Response: {m.content}")
            return m.content == str(confirm) and m.author == ctx.author
        try:
            response = await self.bot.wait_for("message", check=check, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send("Timeout passed. Command aborted!")
            logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Challenge Timed out!")
            return
        else:
            await ctx.send("Authenticated!\nGoodbye")
            logger.debug(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Challenge passed!")
            logger.fatal(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Shutting down... || Authorized by: {ctx.author}")
            sys.exit(f"Shutting down... || Authorized by: {ctx.author}")

    @commands.command(help="Gives an Admin the log Files", breif="DM log files")
    @commands.has_guild_permissions(administrator=True)
    async def giveLog(self, ctx:commands.Context):
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Issued command")
        await ctx.author.send(file=discord.File('./logs/log.log'))
        await ctx.author.send(file=discord.File('./logs/log.prev.log'))
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Sent the log files!")

    @commands.command(name="raid", help="Toggle Raid mode for the server.", breif="Toggle raid mode")
    @commands.has_guild_permissions(manage_messages=True)
    async def raidMode(self, ctx:commands.Context):
        logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > Raid mode toggled!")
        with open('./database/raid.db', 'r') as fp:
            raidBool = fp.read()
        if raidBool == "0":
            with open('./database/raid.db', 'w') as fp:
                fp.write("1")
            await ctx.reply("***RAID MODE ENABLED!***\nVerification system suspended.")
            await adminCommandLogs(ctx.author, "ENABLED RAID MODE!", ctx.channel, self.bot)
            logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > RAID MODE ENABLED")
        elif raidBool == "1":
            with open('./database/raid.db', 'w') as fp:
                fp.write("0")
            await ctx.reply("***RAID MODE DISABLED***")
            await adminCommandLogs(ctx.author, "DISABLED RAID MODE!", ctx.channel, self.bot)
            logger.info(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > RAID MODE DISABLED")
        else:
            await ctx.reply("Error!\nMalformed Database. Report this now!")
            logger.fatal(f"[{ctx.author} / {ctx.author.id}] ({ctx.invoked_with}) > MALFORMED DATABASE")
    

    
        

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Admin(bot)
    )