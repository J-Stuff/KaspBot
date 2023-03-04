import discord, time, datetime, os, asyncio, logging, random, sys
from discord.ext import commands
from discord import app_commands
from discord.utils import format_dt
from config.getConfig import settings as preSettings
from modules.logging.userCommandLogs import userCommandLogs
from modules.logging.adminCommandLogs import adminCommandLogs
settings = preSettings()

class adminSlash(commands.Cog, name="Admin Slash Commands"):
    def __init__(self, bot:commands.Bot):
        logging.debug("adminSlash init ran")
        self.bot = bot

    @app_commands.command(name="purge", description="Allows an admin to purge the chat")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purgeChat(self, interaction:discord.Interaction, count: int):
        logging.debug("Purge Ran")
        channel = interaction.channel
        if not channel:
            logging.fatal("Channel is None in purge, Failing!")
            return
        if type(channel) is not discord.TextChannel:
            logging.info("Channel is not textchannel when purge called. Failing!")
            return
        await interaction.response.defer(ephemeral=False, thinking=True)
        logging.debug("Interaction Deferred")
        logging.debug("Beginning purge...")
        purged = await channel.purge(limit=count)
        logging.debug("Purge complete!")
        logging.debug("Logging purge content...")
        with open('./temp/PURGE.txt', 'w') as fp:
            now = datetime.datetime.utcnow()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            fp.write(f"Purged at: {dt_string} UTC")
            fp.write('\n')
            fp.write(f"Purged by user: {interaction.user} ({interaction.user.id})")
            fp.write('\n')
            fp.write('======================================================')
            fp.write('\n')
            fp.write('\n')
            for message in purged:
                sentAt = message.created_at 
                sent_timeStamp = sentAt.strftime("%d/%m/%Y %H:%M:%S")
                fp.write(f"Author: {message.author} ({message.author.id}) // At: {sent_timeStamp} | Content: {message.content} | Attachments: {message.attachments}")
        logging.debug("Logging of purged content complete!")


        logChannelID = settings.getChannelID("adminLogs")
        logChannel = await self.bot.fetch_channel(int(logChannelID))
        if type(logChannel) is not discord.TextChannel:
            sys.exit("BAD CHANNEL ID FOR: admin_log_channel")
        
        logging.debug("Sending purge log!")
        await logChannel.send("Purge log", file=discord.File('./temp/PURGE.txt'))
        logging.debug("Sent purge log")

        logging.debug("Removing purge file...")
        os.remove("./temp/PURGE.txt")
        logging.debug("Removed purge file")

        logging.debug("Sending purge confirmation...")
        await channel.send(f"Done! Purged `{count}` messages!")
        logging.debug("Sending Admin Log of purge event...")
        await adminCommandLogs(interaction.user, f"Purged {count} messages!", interaction.channel, self.bot)

    @app_commands.command(name="verify", description="Verify a user!")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifyUser(self, interaction:discord.Interaction, target: discord.Member):

        # -----------------------------------------------------
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
            
            await adminCommandLogs(interaction.user, f"/verify\nVerified <@{target.id}> (`{target}` // `{target.id}`)!", interaction.channel, self.bot)
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

        # ---------------------------------------------------------------------------------

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

    @app_commands.command(name="unverified-scan", description="Scan and update the User Registry")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def unvScan(self, interaction:discord.Interaction):
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
        await adminCommandLogs(interaction.user, f"Ran /unverified-scan", interaction.channel, self.bot)

    @app_commands.command(name='ticket-close', description="Close a ticket")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def do_CloseTicket(self, interaction:discord.Interaction, ticket: discord.TextChannel):
        # ------------------------------------------------------------------------------------
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
        # ----------------------------------

        channel = ticket
        from tinydb import TinyDB, Query
        db = TinyDB('./database/tickets.json')
        User = Query()
        if channel.name.startswith("ticket-"):
            await interaction.response.defer(ephemeral=False, thinking=True)
            db.update({"active": False}, User.tid == str(channel.id))
            db.close()
            ticketMessages = channel.history(oldest_first=True)
            await ticketLog(ticketMessages, interaction.user, self.bot)
            await channel.delete(reason="Admin Closed this ticket!")
            await adminCommandLogs(interaction.user, f"CLOSED TICKET: {channel.name}", channel, self.bot)
        else:
            await interaction.response.send_message("That is not a ticket channel!", ephemeral=True)

    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def do_warn(self, interaction:discord.Interaction, user:discord.Member, reason:str):
        guild = interaction.guild
        if not guild:
            return
        await interaction.response.defer(thinking=True, ephemeral=True)
        user_warnEmbed = discord.Embed(title='You have received a Warn!', description=f"You recieved a warn from {guild.name}")
        user_warnEmbed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        user_warnEmbed.add_field(name="Reason", value=reason)

        try:
            await user.send(embed=user_warnEmbed)
        except discord.Forbidden:
            await interaction.followup.send("This user either has blocked me, or has their DM's disabled for this server!\nI cannot send a message to them.", ephemeral=True)
        except:
            await interaction.followup.send("This user either has blocked me, or has their DM's disabled for this server!", ephemeral=True)
        else:
            await interaction.followup.send("Done!, I sent the user the following message:", embed=user_warnEmbed, ephemeral=True)
            await adminCommandLogs(interaction.user, f"Warned User: {user}, for {reason}", interaction.channel, self.bot)

    @app_commands.command(name="unverified-kick", description="Run the kick operation for unverified users")
    @app_commands.checks.has_permissions(administrator=True)
    async def do_unverifiedKick(self, interaction:discord.Interaction):
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
            response = await self.bot.wait_for("message", check=check, timeout=20)
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
                    joined = user.joined_at
                    if not joined:
                        continue
                    if joined - datetime.timedelta(days=14) == 0:
                        logging.debug("is over 2 weeks, kicking!")
                        await interaction.followup.send(f"Kicking {user.name}", ephemeral=True)
                        await user.kick(reason="Kicked due to unverified scan!")
                        await interaction.followup.send(f"Kicked {user.mention} // Reason: Kicked due to unverified scan", ephemeral=True)
                        await adminCommandLogs(interaction.user, f"Kicked {user.mention} during unverified purge", interaction.channel, self.bot) 
                else:
                    logging.debug("is clear")

            await interaction.followup.send("All done!")

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError
    ):
        from modules.botMaintenance.appCommand_Errors import appCommand_Error
        await appCommand_Error(interaction, error, self.bot)

class userSlash(commands.Cog, name="User Slash Commands"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name="boop", description="Boop a user")
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def userBoop(self, interaction:discord.Interaction, user:discord.Member|discord.User):
        with open('./database/boops.db', 'r') as fp:
            boopList = fp.read().splitlines()
            boop = random.choice(boopList)
            await userCommandLogs(interaction.user, f"/boop on {user.mention}", interaction.channel, self.bot)
            await interaction.response.send_message(f"{interaction.user.mention} *boops* {user.mention}")
            channel = interaction.channel
            if not channel or type(channel) is not discord.TextChannel:
                return
            await channel.send(boop)

    @app_commands.command(name="lookup", description="Look up a user")
    @app_commands.checks.cooldown(3, 120, key=lambda i: (i.guild_id, i.user.id))
    async def lookup(self, interaction:discord.Interaction, target:discord.User|discord.Member):
        guild = interaction.guild
        if not guild:
            return
        user:discord.User = await self.bot.fetch_user(target.id)
        try:
            member = await guild.fetch_member(target.id)
        except discord.NotFound:
            member = None
        
        if member:
            embed = discord.Embed(title="User Lookup:", description=f"I found {user.display_name}!", timestamp=datetime.datetime.now(), color=discord.colour.parse_hex_number("fcfcfc"))
        else:
            embed = discord.Embed(title="User Lookup:", description=f"I found {user.display_name}!\nHowever, They are not in this server so I'll only have limited information.", timestamp=datetime.datetime.now(), color=discord.colour.parse_hex_number("fcfcfc"))
        embed.add_field(name="User info:", value=f"Username: **-** `{user.name}#{user.discriminator}`\nAccount Created: **-** {format_dt(user.created_at, 'D')} @ {format_dt(user.created_at, 'T')}\nUser Avatar **-** [LINK]({user.display_avatar.url})", inline=False)
        if member:
            roleStr = ""
            for role in member.roles:
                roleStr += f"{role.mention} "
            embed.add_field(name="Roles", value=roleStr, inline=False)
            joined = member.joined_at
            if not joined:
                return
            embed.add_field(name="Joined Server", value=format_dt(joined, "D") + " // " + format_dt(joined, "R"))
        await interaction.response.send_message(embed=embed)
        

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError
    ):
        from modules.botMaintenance.appCommand_Errors import appCommand_Error
        await appCommand_Error(interaction, error, self.bot)


async def setup(bot: commands.Bot):
    logging.info(f"{__file__} - Setting up...")
    guildID = int(settings.getMiscId("guildID"))
    await bot.add_cog(
        adminSlash(bot),
        guild=discord.Object(int(guildID))
    )
    await bot.add_cog(
        userSlash(bot),
        guild=discord.Object(int(guildID))
    )
    logging.info("Syncing tree...")
    sync = await bot.tree.sync(guild=discord.Object(int(guildID)))
    logging.info(str(sync))
    logging.info("Sync of tree complete!")
    logging.info(f"{__file__} - Done!")