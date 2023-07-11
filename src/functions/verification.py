from _kaspBot import KaspBot
from tinydb import TinyDB, Query
from discord.utils import format_dt
import discord, time, datetime, logging, asyncio
from src.modules.logging import Logger as _Logger
from discord.ext import commands
from discord import app_commands


class verificationNotify():
    def __init__(self, bot:KaspBot, user:discord.User|discord.Member) -> None:
        self.bot = bot
        self.user = user
        self.view = discord.ui.View(timeout=None)


    class verifyButton(discord.ui.Button):
        def __init__(self):
            logging.debug("New verifyButton created!")
            super().__init__(label="Verify", style=discord.ButtonStyle.green)

    class denyButton(discord.ui.Button):
        def __init__(self):
            logging.debug("New denyButton created!")
            super().__init__(label="Deny", style=discord.ButtonStyle.red)

    class userButton(discord.ui.Button):
        def __init__(self, username:str):
            logging.debug(f"New userButton created! | {username}")
            super().__init__(label=username, style=discord.ButtonStyle.gray)


    v_button = verifyButton()
    d_button = denyButton()
               

    async def notify(self, joinReason:str, inviteMethod:list[str], interaction:discord.Interaction, sender:discord.User|discord.Member):

        async def verify(interaction:discord.Interaction):
            if not interaction.user.guild_permissions.manage_roles: #type:ignore
                await interaction.response.send_message("You don't have permission to do this!", ephemeral=True)
                logging.info(f"{interaction.user.name} Tried to verify a user but failed check for `guild_permissions.manage_roles`")
                return
            user = self.user
            guild = interaction.guild
            channel = interaction.channel

            if type(channel) is not discord.TextChannel:
                logging.fatal("if type(channel) is not discord.TextChannel: FAILED")
                return
            if type(user) is not discord.Member:
                logging.fatal("if type(user) is not discord.Member: FAILED")
                return
            if not guild:
                logging.fatal("if not guild: FAILED")
                return
            roles:list = [self.bot.EnumMainGuild.ROLES.value.MEMBER]
            unverifiedRoleID:int = self.bot.EnumMainGuild.ROLES.value.UNVERIFIED
            unverifiedRole = guild.get_role(unverifiedRoleID)
            if not unverifiedRole:
                raise Exception("UNVERIFIED ROLE BAD!")
            targetRoles:list[int] = []
            for role in roles:
                targetRoles.append(guild.get_role(role).) #type:ignore
            logging.debug(f"Target Roles for Verification are: {targetRoles}")
            await user.add_roles(targetRoles) #type:ignore
            await user.remove_roles(unverifiedRole)

            welcomeChannel = await guild.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.MAIN)
            if not welcomeChannel:
                raise Exception("BAD welcomeChannel in config")
            welcomeEmbed = discord.Embed(title="Welcome!", description=f"Welcome {user.mention}!")
            welcomeEmbed.add_field(name="Verified by:", value=interaction.user.mention)

            log = _Logger(self.bot)
            await log.AdminLogging(interaction.user, interaction.channel, f"Verified {user.mention}")

            self.d_button.disabled = True
            self.v_button.disabled = True
            self.v_button.style = discord.ButtonStyle.blurple
            self.view.stop()
            self.view.add_item(self.userButton(interaction.user.name))
            await notifMessage.edit(view=self.view)

            await welcomeChannel.send(user.mention, embed=welcomeEmbed) #type:ignore


            confEmbed = discord.Embed(title="Verification", description="Verification Complete!", timestamp=datetime.datetime.utcnow())
            confEmbed.add_field(name="User:", value=f"{user.mention}")
            await interaction.response.send_message(embed=confEmbed, ephemeral=True)

        # ========


        async def deny(interaction:discord.Interaction):
            class denyModal(discord.ui.Modal):
                def __init__(self, bot:KaspBot, denyButton:verificationNotify.denyButton, acceptButton:verificationNotify.verifyButton, view:discord.ui.View) -> None:
                    self.bot = bot
                    self.denyButton = denyButton
                    self.acceptButton = acceptButton
                    self.view = view
                    super().__init__(title="Verification")

                denyReason = discord.ui.TextInput(label="Reason for denying verification", style=discord.TextStyle.long, max_length=2000)

                async def on_submit(self, interaction: discord.Interaction):
                    if type(user) != discord.Member:
                        await interaction.response.send_message("I cannot find this user anymore. They likely left the server!. Denying the verification Request...", ephemeral=True)
                        self.acceptButton.disabled = True
                        self.denyButton.disabled = True
                        self.denyButton.style = discord.ButtonStyle.blurple
                        await notifMessage.edit(view=self.view)
                        self.view.stop()
                        return

                    if self.denyReason.value == None:
                        denyMessage = f"Your verification request in {interaction.guild.name} was denied by {interaction.user.mention} ({interaction.user}) for the reason:\n`NONE PROVIDED`" #type:ignore
                    else:
                        denyMessage = f"Your verification request in {interaction.guild.name} was denied by {interaction.user.mention} ({interaction.user}) for the reason:\n`{self.denyReason.value}`" #type:ignore
                    try:
                        await user.send(denyMessage)
                    except:
                        await interaction.followup.send(f"{user.mention} has their DM's disabled.", ephemeral=True)
                    await user.kick(reason=f"Kicked by {interaction.user} due to failed verification")
                    log = _Logger(self.bot)
                    channel = interaction.channel
                    if type(channel) is not discord.TextChannel:
                        return
                    await log.AdminLogging(interaction.user,interaction.channel, f"Failed Verification Request from {user.mention} / {user.id}", )

            if not interaction.user.guild_permissions.manage_roles: #type:ignore
                await interaction.response.send_message("You don't have permission to do this!", ephemeral=True)
                return
            user = self.user
            await interaction.response.send_modal(denyModal(self.bot, self.d_button, self.v_button, self.view))


        # ========================================================================================================================================================================================================

        verifEmbed = discord.Embed(title="Verification Request!", timestamp=datetime.datetime.utcnow())
        verifEmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
        verifEmbed.add_field(name="User:", value=f"`{interaction.user}`\n`{interaction.user.id}`\n{interaction.user.mention}", inline=False)
        verifEmbed.add_field(name="Account Age:", value=format_dt(interaction.user.created_at, "F"), inline=False)
        verifEmbed.add_field(name="Join Reason:", value=joinReason, inline=False)
        verifEmbed.add_field(name="Invite Method:", value=inviteMethod[0], inline=False)
        verifEmbed.add_field(name="Agrees to the rules:", value="Yes", inline=False)

        self.v_button.callback = verify
        self.v_button.custom_id = str(interaction.user.id)
        self.view.add_item(self.v_button)
        self.d_button.callback = deny
        self.d_button.custom_id = str(interaction.user.id) + str(interaction.user.id)
        self.view.add_item(self.d_button)


        

        verifLogChannel = await self.bot.fetch_channel(self.bot.EnumMainGuild.CHANNELS.value.VERIFICATION_LOGGING)
        if not isinstance(verifLogChannel, discord.TextChannel):
            raise Exception("verificationRequestChannel is bad!")
        self.bot.add_view(self.view)
        notifMessage = await verifLogChannel.send(embed=verifEmbed, view=self.view)




class verificationModal(discord.ui.Modal):
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        self.verificationDatabaseLocation = './data/databases/verification/verification.db'
        super().__init__(title="Verification")

    def getDB(self) -> TinyDB:
        return TinyDB(self.verificationDatabaseLocation)
    
    joinReason = discord.ui.TextInput(label="Why did you join our server?", style=discord.TextStyle.long, min_length=10 ,max_length=200, required=True)
    inviteMethod = discord.ui.Select(placeholder="[OPTIONAL] How were you invited to our server?", min_values=0, max_values=1, options=[discord.SelectOption(label="TikTok", value="TikTok", description="Received the invite from TikTok"), discord.SelectOption(label="Disboard", value="Disboard", description="Found our server on Disboard!"), discord.SelectOption(label="Invited by a friend", value="Friend", description="Invited by a friend currently in this server!"), discord.SelectOption(label="Other", value="Other", description="Other means of invite (Vanity URL, ETC)")])
    rulesAgree = discord.ui.Select(placeholder="Do you agree to the rules listed in the rules channel?", min_values=1, max_values=1, options=[discord.SelectOption(label="Yes", value="Y"), discord.SelectOption(label="No", value="N")])

    async def on_submit(self, interaction: discord.Interaction):
        if self.rulesAgree.values == ["N"]:
            await interaction.response.send_message("You didn't agree to the server rules, Please read them then choose 'Y' if you accept them next time.")
            return
        db = self.getDB()
        db.insert({"id": str(interaction.user.id)})
        n = verificationNotify(self.bot, interaction.user)
        await n.notify(self.joinReason.value, self.inviteMethod.values, interaction, interaction.user)

class VerificationView(discord.ui.View):
    def __init__(self, bot:KaspBot):
        self.bot = bot
        self.ageReq = 7
        super().__init__(timeout=None)


    class database():
        def __init__(self, ageReq:int) -> None:
            self.ageReq = ageReq
            self.raidFileLocation = './data/verification/raid.bin'
            self.verificationDatabaseLocation = './data/verification/verification.db'

        
        def getDB(self) -> TinyDB:
            return TinyDB(self.verificationDatabaseLocation)
        
        def checkForUser(self, id:int) -> bool:
            """Checks for user in the verification Database

            Args:
                id (int): The Discord UUID of the user we are checking for

            Returns:
                bool: The bool returned, True = The user was found in the database. False = They were not found.
            """
            db = self.getDB()
            User = Query()
            result = db.search(User.id == str(id))
            if len(result) != 0:
                return True
            else:
                return False
            
        def isAccountTooYoung(self, user:discord.User|discord.Member) -> bool:
            """Checks if the account passed was created before the time period specified in the config

            Args:
                user (discord.User | discord.Member): The User/Member we are checking

            Returns:
                bool: If the account is too young. True = The account is too young. False = The account is old enough
            """
            created = user.created_at
            now = datetime.datetime.now()
            if now - created < datetime.timedelta(days=self.ageReq):
                return True
            else:
                return False
            
        def isRaidMode(self) -> bool:
            """Checks if Raid mode is enabled

            Returns:
                bool: Raid mode boolean
            """
            with open(self.raidFileLocation, 'r') as fp:
                raid = fp.read()
            if raid == "0":
                return False
            elif raid == "1":
                return True
            else:
                with open(self.raidFileLocation, 'w') as fp:
                    fp.write("0")
                    fp.close()
                return False


    @discord.ui.button(label="Verify!", custom_id="VerificationButton", style=discord.ButtonStyle.green, emoji="✅")
    async def verify(self, interaction:discord.Interaction, button:discord.ui.Button):
        db = self.database(self.ageReq)
        if db.isAccountTooYoung(interaction.user):
            await interaction.response.send_message(f"Your account is too young to verify!\nPlease wait until your account is at least `{self.ageReq}` days old before verifying.", ephemeral=True)
            return
        
        if db.checkForUser(interaction.user.id):
            await interaction.response.send_message("You are already queued for Verification!", ephemeral=True)
            return
        
        if db.isRaidMode():
            await interaction.response.send_message("Raid mode is currently enabled, please try again later", ephemeral=True)
            return
        
        await interaction.response.send_modal(verificationModal(self.bot))


class VerificationCommands(commands.Cog):
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        super().__init__()


    @app_commands.command(name="verify", description="Verify a user!")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verifyUser(self, interaction:discord.Interaction, target: discord.Member):

        # -----------------------------------------------------
        async def giveVerRole(interaction:discord.Interaction):
            guild = interaction.guild
            if guild == None:
                await interaction.response.send_message("FAILURE <!>\nReport this NOW (Screenshot me! WIN KEY + Shift + S)\n`giveVerRole - guild == None`\n0", ephemeral=True)
                return
            

            memberRole = guild.get_role(self.bot.EnumMainGuild.ROLES.value.MEMBER)
            unv_role = guild.get_role(self.bot.EnumMainGuild.ROLES.value.UNVERIFIED)        
            updatedTarget = await guild.fetch_member(target.id)

            if memberRole in updatedTarget.roles: 
                await interaction.response.send_message("User is already verified!", ephemeral=True)
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
            
            await _Logger(self.bot).AdminLogging(interaction.user, interaction.channel, f"/verify\nVerified <@{target.id}> (`{target}` // `{target.id}`)!")
            try:
                await target.send(f"Your verification request in {target.guild.name} was manually overridden. Welcome!")
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


    @commands.command(name='sendVerEmbed', description="Send the verification embed to a channel")
    @commands.has_guild_permissions(manage_roles=True)
    async def sendVerEmbed(self, ctx:commands.Context):
        await ctx.reply("Sending verification embed to the channel you are in! (deleting this in 5 seconds)", delete_after=5)
        await ctx.send(embed=discord.Embed(title="Verification", description="Click the button below to verify yourself!", color=discord.colour.parse_hex_number("ffcc00")), view=VerificationView(self.bot))
        self.bot.add_view(VerificationView(self.bot))
        await asyncio.sleep(5)
        await ctx.message.delete()