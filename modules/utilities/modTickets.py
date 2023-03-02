import discord
import time
import sys
import random
import datetime
import os
import logging
from discord.utils import get
from modules.logging.userCommandLogs import userCommandLogs
from config.getConfig import settings as unsettings
settings = unsettings()
from modules.logging.adminCommandLogs import adminCommandLogs
from discord.ext import commands



# Databases look like this:
# "tid": str(channel.id),
# "uid": str(interaction.user.id),
# "active": True,
# "ticketOpened": unix

async def ticketLog(messages, closedBy:discord.User|discord.Member, bot:commands.Bot):
    fileID = str(random.randint(1111, 9999))
    with open(f'./temp/{fileID}.txt', 'a') as fp:
        now = datetime.datetime.utcnow()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        fp.write(f"Closed at: {dt_string} UTC")
        fp.write('\n')
        fp.write(f"Closed by user: {closedBy} ({closedBy.id})")
        fp.write('\n')
        fp.write('======================================================')
        fp.write('\n')
        fp.write('\n')
        async for line in messages:
            if not line.author == bot.user:
                sentAt = line.created_at 
                sent_timeStamp = sentAt.strftime("%d/%m/%Y %H:%M:%S")
                fp.write(f"Author: {line.author} ({line.author.id}) // At: {sent_timeStamp} | Content: {line.content}")
                fp.write('\n')
    logChannel = bot.get_channel(int(settings.getChannelID("ticketLogs")))
    embed = discord.Embed(title="A ticket was closed", color=discord.colour.parse_hex_number("0099ff"))
    unix = int(time.time())
    embed.add_field(name="Closed on:", value=f"<t:{unix}:F>\n(<t:{unix}:R>)")
    embed.add_field(name="Closed by:", value=closedBy.mention)
    await logChannel.send(embed=embed, file=discord.File(f"./temp/{fileID}.txt")) #type:ignore
    time.sleep(1)
    os.remove(f"./temp/{fileID}.txt")
        
        
async def closeTicket(interaction:discord.Interaction, ticket: discord.TextChannel, bot):
    channel = ticket
    from tinydb import TinyDB, Query
    db = TinyDB('./database/tickets.json')
    User = Query()
    if channel.name.startswith("ticket-"):
        await interaction.response.defer(ephemeral=False, thinking=True)
        db.update({"active": False}, User.tid == str(channel.id))
        db.close()
        ticketMessages = channel.history(oldest_first=True)
        await ticketLog(ticketMessages, interaction.user, bot)
        await channel.delete(reason="Admin Closed this ticket!")
        await adminCommandLogs(interaction.user, f"CLOSED TICKET: {channel.name}", channel, bot)
    else:
        await interaction.response.send_message("That is not a ticket channel!", ephemeral=True)

    
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


