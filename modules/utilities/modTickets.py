import discord
import time
import json
import random
import tinydb
import datetime
import os
from discord.utils import get
from modules.logging.userCommandLogs import userCommandLogs
from modules.logging.adminCommandLogsMessage import adminCommandLogsMessage
from modules.config.loadConfigs import botConfig

async def ticketLog(messages, closedBy, bot):
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
    logChannel = bot.get_channel(botConfig()["ticket_log_channel"])
    embed = discord.Embed(title="A ticket was closed", color=discord.colour.parse_hex_number("0099ff"))
    unix = int(time.time())
    embed.add_field(name="Closed on:", value=f"<t:{unix}:F>\n(<t:{unix}:R>)")
    embed.add_field(name="Closed by:", value=closedBy.mention)
    await logChannel.send(embed=embed, file=discord.File(f"./temp/{fileID}.txt"))
    time.sleep(1)
    os.remove(f"./temp/{fileID}.txt")
        
        
async def closeTicket(interaction, ticket: discord.TextChannel, bot):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    channel = ticket
    db = tinydb.TinyDB('./data/tickets.database.json')
    if channel.name.startswith("ticket-"):
        await interaction.response.defer(ephemeral=False, thinking=True)
        TicketDB = tinydb.Query()
        db.update({"active": False}, TicketDB.ticket_id == channel.id)# type:ignore
        db.close()
        ticketMessages = channel.history(oldest_first=True)
        await ticketLog(ticketMessages, interaction.user, bot)
        await channel.delete(reason="Admin Closed this ticket!")
        await adminCommandLogsMessage(interaction.user, f"CLOSED TICKET: {channel.name}", bot)
    else:
        await interaction.response.send_message("That is not a ticket channel!", ephemeral=True)

    
class ModTicket(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

        
    # {"ticket_id": 2394957839487598, "user_id": 983248243232, "active": false, "ticket_opened": 293847239487243987}
        
    @discord.ui.button(label="Open Ticket", custom_id="Open Ticket", style=discord.ButtonStyle.green)
    async def createTicket(self, interaction, button):
        db = tinydb.TinyDB('./data/tickets.database.json')
        user = interaction.user
        TicketDB = tinydb.Query()
        result = db.search(TicketDB.active == True) #type:ignore
        for ticket in result: # type:ignore
            if str(interaction.user.id) in str(ticket["user_id"]):
                await interaction.response.send_message("You already have a ticket open!", ephemeral=True)
                return
        
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(title="Creating Ticket...", description="<a:loader2:1041678096228691980> -- Please wait", color=discord.colour.parse_hex_number("921515"))
        loadingMsg = await interaction.followup.send(embed=embed, ephemeral=True)    
        category = get(interaction.guild.categories, id=botConfig()["reportCategory"])
        channel = await interaction.guild.create_text_channel(f'ticket-{random.randint(1111, 9999)}', category=category)
        unix = int(time.time())
        db.insert({"ticket_id": int(channel.id), "user_id": interaction.user.id, "active": True, "ticket_opened": unix})
        db.close()
        time.sleep(5)
        await channel.set_permissions(user, view_channel=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True)
        time.sleep(1)
        newTicketEmbed = discord.Embed(title=f"New Ticket: {channel.name}", description="Welcome. Please describe your issue below and one of our moderators will respond shortly..", color=discord.colour.parse_hex_number("ff0000"), timestamp=datetime.datetime.now())
        await channel.send(f"<@{user.id}> -- <@&{botConfig()['reportPing']}>", embed=newTicketEmbed)
        embed = discord.Embed(title="Creating Ticket...", description=f"Done! See <#{channel.id}>", color=discord.colour.parse_hex_number("921515"))
        await userCommandLogs(interaction.user, "BUTTON: Create Mod Ticket", interaction.channel, self.bot)
        await interaction.followup.edit_message(message_id=loadingMsg.id, embed=embed)


