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




async def user_verf(interaction:discord.Interaction, target: discord.Member, bot:commands.Bot):
    async def giveVerRole(interaction:discord.Interaction):
        guild = interaction.guild
        if guild == None:
            await interaction.response.send_message("FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - guild == None`\n0", ephemeral=True)
            return
        

        memberRole = guild.get_role(int(settings.getMiscId("memberRole")))
        unv_role = guild.get_role(int(settings.getMiscId("unverifiedID")))        
        updatedTarget = await guild.fetch_member(target.id)

        if memberRole in updatedTarget.roles: 
            await interaction.response.send_message(f"User is already verified!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True, thinking=True)

        embedLoad = discord.Embed(
            title="Verification", color=discord.colour.parse_hex_number("ffcc00"))
        embedLoad.add_field(
            name="Adding Roles", value="Please wait...")
        loader:discord.Message = await interaction.followup.send(embed=embedLoad, ephemeral=True, wait=True)

        if not memberRole:
            await interaction.followup.edit_message(message_id=loader.id, content="FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - if not unv_role`\n0")
            return
        if not unv_role:
            await interaction.followup.edit_message(message_id=loader.id, content="FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - if not ver_role`\n0")
            return
        

        await target.add_roles(memberRole)
        try:
            await target.remove_roles(unv_role)
        except discord.HTTPException:
            logging.error(f"Failed to remove the unverified role from {updatedTarget.id}. They likely didn't have the role!")
        
        await adminCommandLogs(interaction.user, f"/verify\nVerified <@{target.id}> (`{target}` // `{target.id}`)!", interaction.channel, bot)
        try:
            await target.send(f"Your verification request in {target.guild.name} was accepted. Welcome!")
        except discord.Forbidden:
            logging.error(f"Failed to notify {updatedTarget.id} they they have passed verification. They probably have their DM's off.")
        embedDone = discord.Embed(
            title="Verification", color=discord.colour.parse_hex_number("289100"))
        embedDone.add_field(name="Verification Complete",
                            value=f"Welcome, <@{target.id}>!")
        embedDone.set_author(name=interaction.user,
                             icon_url=interaction.user.avatar)
        await interaction.followup.edit_message(message_id=loader.id, embed=embedDone)

    embed = discord.Embed(title="Verification Interface",
                          description=f"Information about: {target}")
    accountCreation = target.created_at
    accountUnix = int(time.mktime(accountCreation.timetuple()))
    embed.add_field(name="Account Created",
                    value=f"<t:{accountUnix}:F>\nWhich was: <t:{accountUnix}:R>", inline=False)
    embed.add_field(
        name='To cancel', value="To cancel this operation, simply ignore this embed and hit 'dismiss message' below", inline=False)
    
    verifyButton = discord.ui.Button(
        label="Verify User", style=discord.ButtonStyle.green)
    verifyButton.callback = giveVerRole
    view = discord.ui.View()
    view.add_item(verifyButton)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def unv_scan(interaction: discord.Interaction, bot: commands.Bot):
    await interaction.response.defer(ephemeral=False, thinking=True)

    guild = interaction.guild
    if not guild:
        return
    members = guild.members
    for member in members:
        member: discord.Member
        if len(member.roles) == 1:
            unv_role = guild.get_role(int(settings.getMiscId("unverifiedID")))  
            if not unv_role:
                await interaction.response.send_message("FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`unv_scan - if not unv_role`\n0")
                return
            await member.add_roles(unv_role)
    
    
    await interaction.followup.send("Done! Updated the User Verification Registry")
    await adminCommandLogs(interaction.user, f"Ran /unverified-scan", interaction.channel, bot)

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

async def unverifiedKick(interaction:discord.Interaction, bot:commands.Bot):
    logging.debug("Running unverifiedKick")
    confirm = random.randint(111, 999)
    logging.debug(f"Confirm code is: {confirm}")
    confirmEmbed = discord.Embed(title="Warning!!!", 
                                description=f"The action you are about to take is **Destructive**\n\nYou are about to kick all unverified members, that have been in the server for more than 14 days.\n\nDo you understand that after starting this action, that it cannot be stopped until complete?\n\nType the following code within 20 seconds to confirm. Or wait for 20 seconds to cancel. \n`{confirm}`",
                                color=discord.colour.parse_hex_number("ff0000"))
    await interaction.response.send_message(embed=confirmEmbed)
    def check(m:discord.Message):
        logging.debug(f"Testing to see if response matches challange code || Challenge code: {confirm} // Response: {m.content}")
        return m.content == str(confirm) and m.author == interaction.user
    try:
        response = await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
        await interaction.followup.send("Timeout passed. Command aborted!")
        logging.debug("Challenge Timed out!")
        return
    else:
        await interaction.followup.send("Authenticated!")
        logging.debug("Challenge passed!")
        
        # ==========================================================

        if interaction.guild == None:
            logging.fatal("Yeah, something majorly fucked up") # https://discord.com/channels/1038438846104338473/1038438847534600255/1080791479544451132
            return
        
        unverifiedRole = interaction.guild.get_role(int(settings.getMiscId("memberRole")))
        verifiedRole = interaction.guild.get_role(int(settings.getMiscId("unverifiedID")))
        async for user in interaction.guild.fetch_members(limit=None):
            logging.debug(user)
            if unverifiedRole in user.roles and verifiedRole not in user.roles:
                logging.debug("is unverified")
                logging.debug(user.joined_at)
                if user.joined_at - datetime.timedelta(days=14) == 0: #type:ignore
                    logging.debug("is over 2 weeks, kicking!")
                    await interaction.followup.send(f"Kicking {user.name}", ephemeral=True)
                    await user.kick(reason="Kicked due to unverified scan!")
                    await interaction.followup.send(f"Kicked {user.mention} // Reason: Kicked due to unverified scan", ephemeral=True)
                    await adminCommandLogs(interaction.user, f"Kicked {user.mention} during unverified purge", interaction.channel, bot) #type:ignore
                    
            else:
                logging.debug("is clear")
        await interaction.followup.send("All done!")