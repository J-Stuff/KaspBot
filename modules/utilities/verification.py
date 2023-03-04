import discord
import sys
import datetime
import logging
from tinydb import TinyDB, Query
from discord.ext import commands
from discord.utils import format_dt
from config.getConfig import settings as unsettings
settings = unsettings()
from logging.adminCommandLogs import adminCommandLogs

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
        await verif.notify(interaction=interaction, q1=self.whyJoin, q2=self.howInvite, q3=self.rulesAgreement, sender=interaction.user.id)
        await interaction.response.send_message("Thanks for your response. I've recorded your answers and sent a notification to the moderators who will review your response and verify your account if you meet our requirements. I'll DM you when that happens!", ephemeral=True)
class verificationNotify():
    def __init__(self, bot:commands.Bot):
            super().__init__()
            self.bot = bot

    class verifyButton(discord.ui.Button):
        def __init__(self):
            super().__init__(label="[Admin] Verify", style=discord.ButtonStyle.green,)

    
    
    async def notify(self, q1, q2, q3, interaction:discord.Interaction, sender:int):
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
        whoIs = discord.ui.Button(style=discord.ButtonStyle.gray, label="Profile", url=f"discord://-/users/{sender}")
        view = discord.ui.View()
        verifyButton = self.verifyButton()
        view.add_item(verifyButton)
        view.add_item(whoIs)

        async def giveVerRole(interaction:discord.Interaction):
            if not interaction.user.guild_permissions.manage_roles: #type:ignore
                await interaction.response.send_message("You don't have permission to do this!", ephemeral=True)
                return
            guild = interaction.guild
            if guild == None:
                await interaction.response.send_message("FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - guild == None`\n0", ephemeral=True)
                return
            

            memberRole = guild.get_role(int(settings.getMiscId("memberRole")))
            unv_role = guild.get_role(int(settings.getMiscId("unverifiedID")))        
            updatedTarget = await guild.fetch_member(sender)

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
            

            await updatedTarget.add_roles(memberRole)
            try:
                await updatedTarget.remove_roles(unv_role)
            except discord.HTTPException:
                logging.error(f"Failed to remove the unverified role from {updatedTarget.id}. They likely didn't have the role!")
            
            await adminCommandLogs(interaction.user, f"/verify\nVerified <@{sender}> (`{sender}`)!", interaction.channel, self.bot)
            try:
                await updatedTarget.send(f"Your verification request in {guild.name} was accepted. Welcome!")
            except discord.Forbidden:
                logging.error(f"Failed to notify {updatedTarget.id} they they have passed verification. They probably have their DM's off.")
            embedDone = discord.Embed(
                title="Verification", color=discord.colour.parse_hex_number("289100"))
            embedDone.add_field(name="Verification Complete",
                                value=f"Welcome, <@{sender}>!")
            embedDone.set_author(name=interaction.user,
                                icon_url=interaction.user.avatar)
            await interaction.followup.edit_message(message_id=loader.id, embed=embedDone)

        verifyButton.callback = giveVerRole
        await notifyChannel.send(embed=embed, view=view)
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