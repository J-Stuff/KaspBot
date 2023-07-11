import discord, datetime, time, Paginator
from discord.ext import commands
from discord import app_commands
from discord.utils import format_dt
from _kaspBot import KaspBot
from src.modules.checks import is_mod
from tinydb import TinyDB, Query



class warn(commands.Cog):
    def __init__(self, bot:KaspBot) -> None:
        self.bot = bot
        self.warningsDBlocation = "./data/warnings/warnings.db" # TinyDB
        super().__init__()


    # Database Structure:

    # {
    #     "user": [INT] Discord ID,
    #     "warnings": [LIST] List of warnings, structured as follows:
    #                 {"time": UNIX, "reason": [STR] WARNING REASON, "moderator": [INT] Discord ID of the moderator, "id": [INT] WARNING ID"}
    # }

    def getDB(self) -> TinyDB:
        return TinyDB(self.warningsDBlocation)
    
    def check_if_user_in_db(self, user:discord.User|discord.Member) -> bool:
        db = self.getDB()
        User = Query()
        result = db.search(User.id == user.id)
        if len(result) == 0:
            return False
        else:
            return True
        
    def purge_user_from_database(self, user:discord.User|discord.Member):
        db = self.getDB()
        User = Query()
        db.remove(User.id == user.id)
    
    def create_data_for_new_user(self, user:discord.User|discord.Member):
        db = self.getDB()
        if self.check_if_user_in_db(user):
            self.purge_user_from_database(user)
        db.insert({"user": user.id, "warnings": []})


    # Chunk a list into smaller lists of a certain size
    def chunk_list(self, list_to_chunk:list, chunk_size:int) -> list[list]:
        return [list_to_chunk[i:i+chunk_size] for i in range(0, len(list_to_chunk), chunk_size)]

    def get_user_data(self, user:discord.User|discord.Member) -> dict|None:
        if not self.check_if_user_in_db(user):
            return None
        db = self.getDB()
        User = Query()
        result = db.search(User.id == user.id)
        return result[0]



    
    def addUserWarn(self, user:discord.User|discord.Member, reason:str, mod:discord.User|discord.Member):
        User = Query()
        db = self.getDB()
        if not self.check_if_user_in_db(user):
            self.create_data_for_new_user(user)
        currentWarnsList:list = db.search(User.id == user.id)[0]["warnings"]
        currentWarnsList.append({"time": int(time.time()), "reason": reason, "moderator": mod.id, "id": len(currentWarnsList) + 1})
        db.update({"warnings": currentWarnsList}, User.id == user.id)
        db.close()

        


    @app_commands.command(name="warn", description="[MOD] Warn a user")
    @app_commands.describe(target="User to Warn")
    @app_commands.describe(reason="Reason for Warning this user")
    @app_commands.guild_only()
    @app_commands.check(is_mod)
    async def warnUser(self, interaction:discord.Interaction, target:discord.User, reason:str):
        warningEmbed = discord.Embed(title="You have received a Warning!", color=discord.colour.Color.brand_red(), description=f"You have received a Warning from {interaction.guild.name}", timestamp=datetime.datetime.now()) #type:ignore // This is for the interaction.guild.name property   
        warningEmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar)
        warningEmbed.add_field(name="Reason:", value=reason)
        warningEmbed.add_field(name="Received from user:", value=interaction.user)
        try:
            await target.send(embed=warningEmbed)
            await interaction.response.send_message("I successfully warned the user. The following embed was sent to them:", embed=warningEmbed, ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I failed to send the warn notification to the user. They probably have their DM's off! (I will still log this warning on my end)", ephemeral=True, embed=warningEmbed)
        except Exception as e:
            await interaction.response.send_message(f"Something failed on my end!\n ```{e}```", ephemeral=True)
            return
        try:
            self.addUserWarn(target, reason, interaction.user)
        except Exception as e1:
            await interaction.followup.send(f"CAUGHT EXCEPTION! (REPORT THIS!!)\n```{e1}```", ephemeral=True)

    @app_commands.command(name="warn-lookup", description="[MOD] Lookup previous warnings for a user")
    @app_commands.describe(target="User to check")
    @app_commands.guild_only()
    @app_commands.check(is_mod)
    async def checkForWarn(self, interaction:discord.Interaction, target:discord.User|discord.Member):
        if not self.check_if_user_in_db(target):
            await interaction.response.send_message("This user isn't in my database. They haven't had any warns.", ephemeral=True)
            return
        data = self.get_user_data(target)
        if not data:
            await interaction.response.send_message("This user has no logged warns.", ephemeral=True)
            return
        allWarns = data["warnings"]
        chunkedWarns = self.chunk_list(allWarns, 5)
        pages = []
        for chunk in chunkedWarns:
            embed = discord.Embed(title=f"Warnings for {target}", color=discord.colour.Color.dark_red())
            for warn in chunk:
                embed.add_field(name=f"Warned by {self.bot.get_user(warn['moderator'])}", value=f"**Reason:** {warn['reason']}\n**Time:** {format_dt(datetime.datetime.fromtimestamp(warn['time']))}, **ID:** `{warn['id']}`", inline=False)
            pages.append(embed)
        await Paginator.Simple(
            ephemeral=True,
            PreviousButton=discord.ui.Button(style=discord.ButtonStyle.gray, label='<-'),
            NextButton=discord.ui.Button(style=discord.ButtonStyle.blurple, label="->"),
            ).start(ctx=interaction, pages=pages)
        

    @app_commands.command(name="warn-remove", description="[MOD] Remove a warning from a user")
    @app_commands.describe(target="User to remove warning from")
    @app_commands.describe(warn_id="ID of the warning to remove")
    @app_commands.guild_only()
    @app_commands.check(is_mod)
    async def removeWarn(self, interaction:discord.Interaction, target:discord.User|discord.Member, warn_id:int):
        if not self.check_if_user_in_db(target):
            await interaction.response.send_message("This user isn't in my database. They haven't had any warns.", ephemeral=True)
            return
        data = self.get_user_data(target)
        if not data:
            await interaction.response.send_message("This user has no logged warns.", ephemeral=True)
            return
        allWarns = data["warnings"]
        for warn in allWarns:
            if warn["id"] == warn_id:
                allWarns.remove(warn)
                break
        else:
            await interaction.response.send_message("This user doesn't have a warn with that ID.", ephemeral=True)
            return        
        db = self.getDB()
        User = Query()
        db.update({"warnings": allWarns}, User.id == target.id)
        db.close()
        await interaction.response.send_message("I successfully removed the warning from the user.", ephemeral=True)