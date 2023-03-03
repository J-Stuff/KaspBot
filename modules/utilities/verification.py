import discord
import time
import os
import sys
import datetime
import random
import asyncio
import logging
from tinydb import TinyDB, Query
from discord.ext import commands
from modules.logging.adminCommandLogs import adminCommandLogs
from discord.utils import format_dt
from config.getConfig import settings as unsettings
settings = unsettings()

class verificationQuestionare(discord.ui.Modal, title='Verification', ):
    def __init__(self, bot:commands.Bot):
            super().__init__()
            self.bot = bot

    whyJoin = discord.ui.TextInput(label="Why do you want to join our server?", placeholder="Must be a minimum of 100 characters long", min_length=100, max_length=512, style=discord.TextStyle.paragraph)
    howInvite = discord.ui.TextInput(label="How did you get invited to this server?", placeholder="Must be a minimum of 50 characters long", min_length=50, max_length=150, style=discord.TextStyle.long)
    rulesAgreement = discord.ui.TextInput(label="Have you read and agree to the rules", placeholder="YES or NO", min_length=2, max_length=3, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        db = TinyDB('./database/verification.json')
        db.insert({"id": str(interaction.user.id)})
        verif = verificationNotify(self.bot)
        await verif.notify(interaction=interaction, q1=self.whyJoin, q2=self.howInvite, q3=self.rulesAgreement)
        await interaction.response.send_message("Thanks for your response. I've recorded your answers and sent a notification to the moderators who will review your response and verify your account if you meet our requirements. I'll DM you when that happens!", ephemeral=True)
class verificationNotify():
    def __init__(self, bot:commands.Bot):
            super().__init__()
            self.bot = bot
    
    async def notify(self, q1, q2, q3, interaction:discord.Interaction):
        verificationNotificationChannel = settings.getChannelID("verificationNotif")
        if verificationNotificationChannel == None:
            logging.info("BAD SETTING verificationNotificationChannel")
            sys.exit()
        notifyChannel = self.bot.get_channel(int(verificationNotificationChannel))
        if notifyChannel == None or type(notifyChannel) is not discord.TextChannel :
            logging.info("BAD SETTING verificationNotificationChannel")
            sys.exit()
        embed = discord.Embed(title="Verification Request", description=f"Account created {format_dt(interaction.user.created_at, 'D')} @ {format_dt(interaction.user.created_at, 'T')}\n(Which was: {format_dt(interaction.user.created_at, 'R')})", color=discord.colour.parse_hex_number("22942f"))
        embed.add_field(name="Response 1: Why do you want to join our server?", value=q1, inline=False)
        embed.add_field(name="Response 2: How did you get invited to this discord server?", value=q2, inline=False)
        embed.add_field(name="Response 3: Have you read and agree to the rules listed in the Rules Channel?", value=q3, inline=False)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        await notifyChannel.send(embed=embed)
class verificationClass(discord.ui.View):
    def __init__(self, bot):
            super().__init__(timeout=None)
            self.bot = bot

    def checkForUser(self, id:str):
        db = TinyDB('./database/verification.json')
        User = Query()
        result = db.search(User.id == id)
        if len(result) is not 0:
            return True
        else:
            return False

    @discord.ui.button(label="Request Verification!", custom_id="VerificationInteraction", style=discord.ButtonStyle.green)
    async def verificationButton(self, interaction:discord.Interaction, button):
        now = datetime.datetime.now()
        created = interaction.user.created_at
        elapsed = now - created
        if self.checkForUser(str(interaction.user.id)) == True:
            await interaction.response.send_message("You have already sent in a request for verification!", ephemeral=True)
            return
        elif elapsed.days < 7:
            await interaction.response.send_message("Your account is too young! Please wait until your account is at least 7 days old before verifying.")
            return
        else:
            await interaction.response.send_modal(verificationQuestionare(self.bot))