import discord
import time
import sys
import random
import datetime
import os
import logging
from discord.utils import get
from modules.logging.userCommandLogs import userCommandLogs
from config.getSetting import getSetting
from modules.logging.adminCommandLogs import adminCommandLogs
from discord.ext import commands

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
    logChannel = bot.get_channel(int(getSetting(os.getenv("SETTINGS_ticketLog"))))
    embed = discord.Embed(title="A ticket was closed", color=discord.colour.parse_hex_number("0099ff"))
    unix = int(time.time())
    embed.add_field(name="Closed on:", value=f"<t:{unix}:F>\n(<t:{unix}:R>)")
    embed.add_field(name="Closed by:", value=closedBy.mention)
    await logChannel.send(embed=embed, file=discord.File(f"./temp/{fileID}.txt")) #type:ignore
    time.sleep(1)
    os.remove(f"./temp/{fileID}.txt")
        
        
async def closeTicket(interaction:discord.Interaction, ticket: discord.TextChannel, bot):
    if not interaction.user.guild_permissions.manage_messages: #type:ignore
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    channel = ticket
    from pymongo import MongoClient
    CONNECTION_STRING = os.getenv("MONGO_connection_string")
    client: MongoClient = MongoClient(CONNECTION_STRING)
    database = os.getenv("MONGO_maindb")
    if database == None:
        logging.info("BAD ENV MONGO_maindb")
        sys.exit()
    db = client[database]
    collection = getSetting(os.getenv("SETTINGS_mongTickCollection"))
    ticketCollection = db[collection]
    if channel.name.startswith("ticket-"):
        await interaction.response.defer(ephemeral=False, thinking=True)
        filter = {"_id": str(channel.id)}
        payload = { "$set": { 'active': False } }
        ticketCollection.update_one(filter, payload, upsert=True)
        ticketMessages = channel.history(oldest_first=True)
        await ticketLog(ticketMessages, interaction.user, bot)
        await channel.delete(reason="Admin Closed this ticket!")
        await adminCommandLogs(interaction.user, f"CLOSED TICKET: {channel.name}", channel, bot)
    else:
        await interaction.response.send_message("That is not a ticket channel!", ephemeral=True)

    
class ModTicket(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        
    @discord.ui.button(label="Open Ticket", custom_id="Open Ticket", style=discord.ButtonStyle.green)
    async def createTicket(self, interaction:discord.Interaction, button):
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        db = client[database]
        collection = getSetting(os.getenv("SETTINGS_mongTickCollection"))
        ticketCollection = db[collection]
        cursor = ticketCollection.find({"active": True})
        activeTickets = list(cursor)
        for ticket in activeTickets:
            if str(interaction.user.id) in ticket["userId"]:
                await interaction.response.send_message("You already have a ticket open!")
                return
                
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(title="Creating Ticket...", description="<a:loader2:1041678096228691980> -- Please wait", color=discord.colour.parse_hex_number("921515"))
        loadingMsg:discord.Message = await interaction.followup.send(embed=embed, ephemeral=True) #type:ignore    
        category = get(interaction.guild.categories, id=getSetting("reportCategory")) #type:ignore
        channel = await interaction.guild.create_text_channel(f'ticket-{random.randint(1111, 9999)}', category=category) #type:ignore
        unix = int(time.time())
        payload = {
            "_id": str(channel.id),
            "userId": str(interaction.user.id),
            "active": True,
            "ticketOpened": unix
        }
        ticketCollection.insert_one(payload)
        time.sleep(5)
        await channel.set_permissions(interaction.user, view_channel=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True) #type:ignore
        time.sleep(1)
        newTicketEmbed = discord.Embed(title=f"New Ticket: {channel.name}", description="Welcome. Please describe your issue below and one of our moderators will respond shortly..", color=discord.colour.parse_hex_number("ff0000"), timestamp=datetime.datetime.now())
        await channel.send(f"<@{interaction.user.id}> -- <@&{getSetting(os.getenv('SETTINGS_reportPing'))}>", embed=newTicketEmbed)
        embed = discord.Embed(title="Creating Ticket...", description=f"Done! See <#{channel.id}>", color=discord.colour.parse_hex_number("921515"))
        await userCommandLogs(interaction.user, "BUTTON: Create Mod Ticket", interaction.channel, self.bot) #type:ignore
        await interaction.followup.edit_message(message_id=loadingMsg.id, embed=embed)


