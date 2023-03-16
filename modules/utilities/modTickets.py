import discord
import time
import random
import datetime
import logging
from discord.utils import get
from modules.logging.userCommandLogs import userCommandLogs
from modules.config.getConfig import settings as unsettings
settings = unsettings()
from discord.ext import commands
class ModTicket(discord.ui.View):
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot
        
    @discord.ui.button(label="Open Ticket", custom_id="Open Ticket", style=discord.ButtonStyle.green)
    async def createTicket(self, interaction:discord.Interaction, button):
        guild = interaction.guild
        if not guild:
            return
        from tinydb import TinyDB, Query
        db = TinyDB('./database/tickets.json')
        User = Query()
        activeTickets = db.search((User.uid == interaction.user.id) & (User.active == True))
        if len(activeTickets) is not 0:
            await interaction.response.send_message("You already have a ticket open!", ephemeral=True)
            return
                        
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(title="Creating Ticket", description="Please wait...", color=discord.colour.parse_hex_number("921515"))
        loadingMsg:discord.Message = await interaction.followup.send(embed=embed, ephemeral=True) #type:ignore    
        category = get(guild.categories, id=int(settings.getChannelID("reportCATEGORY")))
        UID = str(interaction.user.id)
        ticketID = ""
        for i in range(6):
            ticketID += random.choice(UID)
        channel = await guild.create_text_channel(f'ticket-{ticketID}', category=category)
        unix = int(time.time())
        payload = {
            "tid": str(channel.id),
            "uid": str(interaction.user.id),
            "active": True,
            "ticketOpened": unix
        }
        db.insert(payload)
        db.close()
        await channel.set_permissions(interaction.user, view_channel=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True) #type:ignore
        newTicketEmbed = discord.Embed(title=f"New Ticket: {channel.name}", description="Welcome. Please describe your issue below and one of our moderators will respond shortly..", color=discord.colour.parse_hex_number("ff0000"), timestamp=datetime.datetime.now())
        pingPayload = ""
        for id in settings.getMiscId("reportPing"):
            targetRole = (guild.get_role(int(id)))
            if not targetRole:
                logging.warning(f"I can't find the role with the ID of: {id}")
                continue
            pingPayload += targetRole.mention
            pingPayload += " "
        await channel.send(f"<@{interaction.user.id}> -- {pingPayload}", embed=newTicketEmbed)
        embed = discord.Embed(title="Created Ticket", description=f"Done! See <#{channel.id}>", color=discord.colour.parse_hex_number("921515"))
        await userCommandLogs(interaction.user, "BUTTON: Create Mod Ticket", interaction.channel, self.bot)
        await interaction.followup.edit_message(message_id=loadingMsg.id, embed=embed)