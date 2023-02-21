import discord
import time
import os
import sys
import datetime
import random
import asyncio
import logging
from discord.ext import commands
from modules.logging.adminCommandLogs import adminCommandLogs
from config.getSetting import getSetting
from discord.utils import format_dt



async def user_verf(interaction:discord.Interaction, target: discord.Member, bot:commands.Bot):
    if not interaction.user.guild_permissions.manage_roles: #type:ignore
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return

    async def giveVerRole(interaction:discord.Interaction):
        role = target.guild.get_role(int(getSetting("baseRole")))
        guild = interaction.guild
        if guild == None:
            await interaction.response.send_message("FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - guild == None`\n0", ephemeral=True)
            return
        updatedTarget = await guild.fetch_member(target.id)
        if role in updatedTarget.roles:  # type: ignore
            await interaction.response.send_message(f"User is already verified!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=False, thinking=True)
        embedLoad = discord.Embed(
            title="Verification", color=discord.colour.parse_hex_number("ffcc00"))
        embedLoad.add_field(
            name="Adding Roles", value="<a:loader2:1041678096228691980> Please wait...")
        loader = await interaction.followup.send(embed=embedLoad, ephemeral=False)
        guild = None
        guild = bot.get_guild(int(getSetting("guild")))
        if guild == None:
            await interaction.followup.edit_message(message_id=loader.id, content="FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - guild == None`\n1") #type:ignore
            return
        unv_role = guild.get_role(int(getSetting("unverifiedRoleId")))
        ver_role = guild.get_role(int(getSetting("baseRole")))
        if not unv_role:
            await interaction.followup.edit_message(message_id=loader.id, content="FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - if not unv_role`\n0") #type:ignore
            return
        if not ver_role:
            await interaction.followup.edit_message(message_id=loader.id, content="FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - if not ver_role`\n0") #type:ignore
            return
        await target.add_roles(ver_role)
        await target.remove_roles(unv_role)
        await adminCommandLogs(interaction.user, f"/verify\nVerified <@{target.id}> (`{target}` // `{target.id}`)!", interaction.channel, bot) #type:ignore
        try:
            await target.send(f"Your verification request in {target.guild.name} was accepted. Welcome!")
        except:
            pass
        embedDone = discord.Embed(
            title="Verification", color=discord.colour.parse_hex_number("289100"))
        embedDone.add_field(name="Verification Complete",
                            value=f"Welcome, <@{target.id}>!")
        embedDone.set_author(name=interaction.user,
                             icon_url=interaction.user.avatar)
        await interaction.followup.edit_message(message_id=loader.id, embed=embedDone) #type:ignore

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


async def unv_scan(interaction, bot: commands.Bot):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=False, thinking=True)


    members = interaction.guild.members
    for member in members:
        member: discord.Member
        if len(member.roles) == 1:
            guild = bot.get_guild(int(getSetting("guild")))
            unv_role = guild.get_role( # type:ignore
                int(getSetting("unverifiedRoleId")))  
            await member.add_roles(unv_role)  # type:ignore
    
    
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
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        
        db = client[database]

        collection = getSetting("MONGO_verification_collection")
        if collection == None:
            logging.info("BAD DB MONGO_verification_collection")
            sys.exit()
        
        verification = db[collection]
        payload = {
            "_id": str(interaction.user.id),
            "q1": str(self.whyJoin),
            "q2": str(self.howInvite),
            "q3": str(self.rulesAgreement)
        }
        verification.insert_one(payload)
        verif = verificationNotify(self.bot)
        await interaction.response.send_message("Thanks for your response. I've recorded your answers and sent a notification to the moderators who will review your response and verify your account if you meet our requirements. I'll DM you when that happens!", ephemeral=True)
        await verif.notify(interaction=interaction, q1=self.whyJoin, q2=self.howInvite, q3=self.rulesAgreement)


class verificationNotify():
    def __init__(self, bot:commands.Bot):
            super().__init__()
            self.bot = bot
    
    async def notify(self, q1, q2, q3, interaction:discord.Interaction):
        verificationNotificationChannel = getSetting("verificationNotificationChannel")
        if verificationNotificationChannel == None:
            logging.info("BAD SETTING verificationNotificationChannel")
            sys.exit()
        notifyChannel = self.bot.get_channel(int(verificationNotificationChannel))
        embed = discord.Embed(title="Verification Request", description=f"Account created {format_dt(interaction.user.created_at, 'D')} @ {format_dt(interaction.user.created_at, 'T')}\n(Which was: {format_dt(interaction.user.created_at, 'R')})", color=discord.colour.parse_hex_number("22942f"))
        embed.add_field(name="Response 1: Why do you want to join our server?", value=q1)
        embed.add_field(name="Response 2: How did you get invited to this discord server?", value=q2)
        embed.add_field(name="Response 3: Have you read and agree to the rules listed in the Rules Channel?", value=q3)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) #type:ignore
        await notifyChannel.send(embed=embed) #type:ignore

class verificationClass(discord.ui.View):
    def __init__(self, bot):
            super().__init__(timeout=None)
            self.bot = bot

    def checkForUser(self, id:str):
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        
        db = client[database]

        collection = getSetting(os.getenv("SETTINGS_mongVerifCollection"))
        if collection == None:
            logging.info("BAD ENV SETTINGS_mongVerifCollection")
            sys.exit()
        
        verification = db[collection]

        search = verification.find_one({"_id": id})
        if search == None:
            return False
        else:
            return True

            


    @discord.ui.button(label="Request Verification!", custom_id="VerificationInteraction", style=discord.ButtonStyle.green)
    async def verificationButton(self, interaction:discord.Interaction, button):
        if self.checkForUser(str(interaction.user.id)) == True:
            await interaction.response.send_message("You have already sent in a request for verification!", ephemeral=True)
            return
        elif interaction.user.created_at - datetime.timedelta(days=7) == 0:
            await interaction.response.send_message("Your account is too young! Please wait until your account is at least 7 days old before verifying.")
            return
        else:
            await interaction.response.send_modal(verificationQuestionare(self.bot))

async def unverifiedKick(interaction:discord.Interaction, bot:commands.Bot):
    if interaction.user.guild_permissions.administrator: #type:ignore
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
            logging.fatal("interaction.guild seems to be None?")
            return
        
        unverifiedRole = interaction.guild.get_role(int(getSetting("unverifiedRoleId")))
        verifiedRole = interaction.guild.get_role(int(getSetting("baseRole")))
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