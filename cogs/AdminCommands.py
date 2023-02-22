from discord.ext import commands
from discord import app_commands
from config.getSetting import getSetting
from modules.logging.adminCommandLogs import adminCommandLogs
import discord
import os
import sys
import json
import requests
import random
import logging
import time
import datetime
import asyncio

class Admin(commands.Cog, name="Admin Commands"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    def getCollection(self, collection):
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        db = client[database]
        return db[collection]
        
    # =====================

    @commands.command(help="Shows the bot ping, version & status.", brief="Bot Status.")
    async def status(self, ctx:commands.Context):
        logging.info("running command status")
        if ctx.author.guild_permissions.manage_messages: #type:ignore
            ping_ms = int(self.bot.latency * 1000)
            discord_api = requests.get(
                "https://discordstatus.com/api/v2/summary.json")
            dApiData = json.loads(discord_api.text)
            dApiStatus = dApiData["components"][0]["status"]
            if dApiStatus == "operational":
                operationalMessage = "<:green_heart:1034024591791771648> `Discord API Online`"
            else:
                operationalMessage = "<:broken_heart:1034024591791771648> `Discord API Degraded`"

            with open('./database/uptime.db', 'r') as fp:
                uptimeUnix = float(fp.read())
            uptime = str(datetime.timedelta(seconds=int(round(time.time()-uptimeUnix))))
            info = "1.2.1"
            await ctx.send(f"Pong!\n<:satellite:1034018740897075231> `{str(ping_ms)} ms`\nI'm running KaspBot Version: {info}\nUptime: {uptime}")


    @commands.command(help="Send the embed for reaction roles. Requires manage_guild", brief="Reaction Roles Embed")
    async def sendRRembed(self, ctx: commands.Context):
        from modules.utilities.reactionRolesClasses import SORoles, SpeciesRoles, ColorRoles, GenderRoles, PronounRoles
        logging.info("running command sendRRembed")
        if ctx.author.guild_permissions.manage_guild: #type:ignore
            embed0 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself an orientation role\n_                                                                                                                                                                                                                _",
                                color=discord.colour.parse_hex_number("00a83d"))
            await ctx.send(embed=embed0, view=SORoles(self.bot))

            embed1 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a pronoun role\n_                                                                                                                                                                                                                _",
                                color=discord.colour.parse_hex_number("00a83d"))
            await ctx.send(embed=embed1, view=PronounRoles(self.bot))

            embed2 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a gender role\n_                                                                                                                                                                                                                _",
                                color=discord.colour.parse_hex_number("00a83d"))
            await ctx.send(embed=embed2, view=GenderRoles(self.bot))

            embed3 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a color role\n_                                                                                                                                                                                                                _",
                                color=discord.colour.parse_hex_number("00a83d"))
            await ctx.send(embed=embed3, view=ColorRoles(self.bot))

            embed4 = discord.Embed(title="Reaction Buttons", description="Use the buttons below to assign yourself a species role\n_                                                                                                                                                                                                                _",
                                color=discord.colour.parse_hex_number("00a83d"))
            await ctx.send(embed=embed4, view=SpeciesRoles(self.bot))
            await adminCommandLogs(ctx.author, f"Sent the ReactionRoles Embeds", ctx.channel, self.bot)

    @commands.command(help="Send the report embed. Requires: manage_guild", brief="Send Report Embed")
    async def sendReportEmbed(self, ctx:commands.Context):
        from modules.utilities.modTickets import ModTicket
        logging.info("running command sendSPCembed")
        if ctx.author.guild_permissions.manage_guild: #type:ignore
            embed = discord.Embed(title="Create a Ticket with the Moderators", description="Use the button below to create a ticket to contact our moderators!",
                                color=discord.colour.parse_hex_number("00a83d"))
            await ctx.send(embed=embed, view=ModTicket(self.bot))
            await adminCommandLogs(ctx.author, f"Sent the Report Embed", ctx.channel, self.bot)

    @commands.command(help="Send the verification embed. Requires: manage_guild", brief="Send Verif Embed")
    async def sendVerEmbed(self, ctx:commands.Context):
        from modules.utilities.verification import verificationClass
        if ctx.author.guild_permissions.manage_guild: #type:ignore
            embed = discord.Embed(title="Begin Verification", description="Use the button below to begin Verification!",
                                color=discord.colour.parse_hex_number("00a83d"))
            await ctx.send(embed=embed, view=verificationClass(self.bot))
            await adminCommandLogs(ctx.author, f"Sent the Verification Embed", ctx.channel, self.bot)
        
    @commands.command(help="Reload the bot. Requires: administrator", brief="Reload")
    async def reload(self, ctx:commands.Context):
        if ctx.author.guild_permissions.administrator: #type:ignore
            from modules.botMaintenance.cog_controller import cogController
            controller = cogController(self.bot)
            await ctx.reply("<:arrows_counterclockwise:1077506380463870023> Reloading now...")
            await controller.reloadCogs()
            await ctx.send("Done!")

    @commands.command(help="Echos what is said in the command. Requires: mention_everyone", brief="Echo message")
    async def echo(self, ctx:commands.Context, *, repeat:str):
        if ctx.author.guild_permissions.mention_everyone: #type:ignore
            await ctx.message.delete()
            await ctx.send(f"{repeat}")
            await adminCommandLogs(ctx.author, f"Made me echo: {repeat}", ctx.channel, self.bot)

    @commands.command(help="Shut down the bot. Requires: administrator", breif="Shutdown the Bot")
    async def shutdown(self, ctx:commands.Context):
        if ctx.author.guild_permissions.administrator: #type:ignore
            confirm = random.randint(111, 999)
            logging.debug(f"Confirm code is: {confirm}")
            confirmEmbed = discord.Embed(title="Warning!!!", 
                                        description=f"The action you are about to take is **Destructive**\n\nYou are about to shut me down...\n\nDo you understand that after starting this action, that it cannot be stopped until complete?\n\nType the following code within 20 seconds to confirm. Or wait for 20 seconds to cancel. \n`{confirm}`",
                                        color=discord.colour.parse_hex_number("ff0000"))
            await ctx.send(embed=confirmEmbed)
            def check(m:discord.Message):
                logging.debug(f"Testing to see if response matches challange code || Challenge code: {confirm} // Response: {m.content}")
                return m.content == str(confirm) and m.author == ctx.author
            try:
                response = await self.bot.wait_for("message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send("Timeout passed. Command aborted!")
                logging.debug("Challenge Timed out!")
                return
            else:
                await ctx.send("Authenticated!\nGoodbye")
                logging.debug("Challenge passed!")
                logging.fatal(f"Shutting down... || Authorized by: {ctx.author}")
                sys.exit(f"Shutting down... || Authorized by: {ctx.author}")

    @commands.command(help="Gives an Admin the log Files", breif="DM log files")
    async def giveLog(self, ctx:commands.Context):
        if ctx.author.guild_permissions.administrator: #type:ignore
            await ctx.author.send(file=discord.File('./logs/log.log'))
            await ctx.author.send(file=discord.File('./logs/log.prev.log'))
            
        

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Admin(bot)
    )