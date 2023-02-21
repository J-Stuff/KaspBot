import discord
from discord.ext import commands
import os
import sys
import logging
from modules.logging.userCommandLogs import userCommandLogs
from config.getSetting import getSetting
class SpeciesRoles(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    def getSpeciesDB(self):
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        db = client[database]
        collection = getSetting(os.getenv("SETTINGS_reactionRolesCollection"))
        rrCollection = db[collection]
        result = rrCollection.find_one("speciesRoles")
        if result == None:
            logging.info(' result = rrCollection.find_one("speciesRoles") >> result == None!')
            sys.exit()
        payload = result["value"]
        return payload

    async def applyRole(self, interaction:discord.Interaction, role:str):
        targetRoleID = int(self.getSpeciesDB()[role])
        guild = interaction.guild
        if guild == None:
            logging.info(f"Error: RR00-0 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR00-0 - {role}")
            sys.exit()
        targetRole = guild.get_role(targetRoleID)
        if targetRole == None:
            logging.info(f"Error: RR00-1 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR00-1 - {role}")
            sys.exit()
        user = interaction.user
        if type(user) is not discord.Member:
            logging.info(f"Error: RR00-2 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR00-2 - {role}")
            sys.exit()
        if targetRole in user.roles:
            await user.remove_roles(targetRole)
            await interaction.response.send_message(f"Removed the role `{targetRole.name}` from {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Removed {targetRole.name} Role", interaction.channel, self.bot)
        else:
            await user.add_roles(targetRole)
            await interaction.response.send_message(f"Added the role `{targetRole.name}` to {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Added {targetRole.name} Role", interaction.channel, self.bot)


    @discord.ui.button(label="Avian", custom_id="avian", style=discord.ButtonStyle.blurple)
    async def avianButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "avian")

    @discord.ui.button(label="Bear", custom_id="bear", style=discord.ButtonStyle.blurple)
    async def bearButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "bear")

    @discord.ui.button(label="Canine", custom_id="canine", style=discord.ButtonStyle.blurple)
    async def canineButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "canine")

    @discord.ui.button(label="Deer", custom_id="deer", style=discord.ButtonStyle.blurple)
    async def deerButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "deer")

    @discord.ui.button(label="Derg", custom_id="derg", style=discord.ButtonStyle.blurple)
    async def dergButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "derg")

    @discord.ui.button(label="Dragon", custom_id="dragon", style=discord.ButtonStyle.blurple)
    async def dragonButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "dragon")

    @discord.ui.button(label="Feline", custom_id="feline", style=discord.ButtonStyle.blurple)
    async def felineButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "feline")

    @discord.ui.button(label="Fox", custom_id="fox", style=discord.ButtonStyle.blurple)
    async def foxButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "fox")

    @discord.ui.button(label="Hobkin", custom_id="hobkin", style=discord.ButtonStyle.blurple)
    async def hobkinButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "hobkin")

    @discord.ui.button(label="Kobold", custom_id="kobold", style=discord.ButtonStyle.blurple)
    async def koboldButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "kobold")

    @discord.ui.button(label="Moth", custom_id="moth", style=discord.ButtonStyle.blurple)
    async def mothButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "moth")

    @discord.ui.button(label="Otter", custom_id="otter", style=discord.ButtonStyle.blurple)
    async def otterButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "otter")

    @discord.ui.button(label="Protogen", custom_id="protogen", style=discord.ButtonStyle.blurple)
    async def protogenButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "protogen")

    @discord.ui.button(label="Shark", custom_id="shark", style=discord.ButtonStyle.blurple)
    async def sharkButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "shark")

    @discord.ui.button(label="Skulldog", custom_id="skulldog", style=discord.ButtonStyle.blurple)
    async def skulldogButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "skulldog")

    @discord.ui.button(label="Wickerbeast", custom_id="wickerbeast", style=discord.ButtonStyle.blurple)
    async def wbButton(self, interaction:discord.Interaction, button):
        await self.applyRole(interaction, "wickerbeast")

class ColorRoles(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    def getColorDB(self):
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        db = client[database]
        collection = getSetting(os.getenv("SETTINGS_reactionRolesCollection"))
        rrCollection = db[collection]
        result = rrCollection.find_one("colorRoles")
        if result == None:
            logging.info(' result = rrCollection.find_one("colorRoles") >> result == None!')
            sys.exit()
        payload = result["value"]
        logging.info(payload)
        return payload
    
    async def applyRole(self, interaction:discord.Interaction, role:str):
        targetRoleID = int(self.getColorDB()[role])
        logging.info(targetRoleID)
        guild = interaction.guild
        if guild == None:
            logging.info(f"Error: RR01-0 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR01-0 - {role}")
            sys.exit()
        targetRole = guild.get_role(targetRoleID)
        if targetRole == None:
            logging.info(f"Error: RR01-1 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR01-1 - {role}")
            sys.exit()
        user = interaction.user
        if type(user) is not discord.Member:
            logging.info(f"Error: RR01-2 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR01-2 - {role}")
            sys.exit()
        if targetRole in user.roles:
            await user.remove_roles(targetRole)
            await interaction.response.send_message(f"Removed the role `{targetRole.name}` from {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Removed {targetRole.name} Role", interaction.channel, self.bot)
        else:
            await user.add_roles(targetRole)
            await interaction.response.send_message(f"Added the role `{targetRole.name}` to {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Added {targetRole.name} Role", interaction.channel, self.bot)

    @discord.ui.button(label="Red",  custom_id="red",style=discord.ButtonStyle.blurple)
    async def red(self, interaction, button):
        await self.applyRole(interaction, "red")

    @discord.ui.button(label="Orange", custom_id="orange", style=discord.ButtonStyle.blurple)
    async def orange(self, interaction, button):
        await self.applyRole(interaction, "orange")

    @discord.ui.button(label="Yellow", custom_id="yellow", style=discord.ButtonStyle.blurple)
    async def yellow(self, interaction, button):
        await self.applyRole(interaction, "yellow")

    @discord.ui.button(label="Green", custom_id="green", style=discord.ButtonStyle.blurple)
    async def green(self, interaction, button):
        await self.applyRole(interaction, "green")

    @discord.ui.button(label="Teal", custom_id="teal", style=discord.ButtonStyle.blurple)
    async def teal(self, interaction, button):
        await self.applyRole(interaction, "Teal")

    @discord.ui.button(label="Cyan", custom_id="cyan", style=discord.ButtonStyle.blurple)
    async def cyan(self, interaction, button):
        await self.applyRole(interaction, "cyan")

    @discord.ui.button(label="Blue", custom_id="blue", style=discord.ButtonStyle.blurple)
    async def blue(self, interaction, button):
        await self.applyRole(interaction, "blue")

    @discord.ui.button(label="Purple", custom_id="purple", style=discord.ButtonStyle.blurple)
    async def purple(self, interaction, button):
        await self.applyRole(interaction, "purple")

    @discord.ui.button(label="Pink", custom_id="pink", style=discord.ButtonStyle.blurple)
    async def pink(self, interaction, button):
        await self.applyRole(interaction, "pink")

class SORoles(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
        
    def getSoDB(self):
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        db = client[database]
        collection = getSetting(os.getenv("SETTINGS_reactionRolesCollection"))
        rrCollection = db[collection]
        result = rrCollection.find_one("soRoles")
        if result == None:
            logging.info(' result = rrCollection.find_one("soRoles") >> result == None!')
            sys.exit()
        payload = result["value"]
        return payload

    async def applyRole(self, interaction:discord.Interaction, role:str):
        targetRoleID = int(self.getSoDB()[role])
        guild = interaction.guild
        if guild == None:
            logging.info(f"Error: RR02-0 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR02-0 - {role}")
            sys.exit()
        targetRole = guild.get_role(targetRoleID)
        if targetRole == None:
            logging.info(f"Error: RR02-1 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR02-1 - {role}")
            sys.exit()
        user = interaction.user
        if type(user) is not discord.Member:
            logging.info(f"Error: RR02-2 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR02-2 - {role}")
            sys.exit()
        if targetRole in user.roles:
            await user.remove_roles(targetRole)
            await interaction.response.send_message(f"Removed the role `{targetRole.name}` from {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Removed {targetRole.name} Role", interaction.channel, self.bot)
        else:
            await user.add_roles(targetRole)
            await interaction.response.send_message(f"Added the role `{targetRole.name}` to {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Added {targetRole.name} Role", interaction.channel, self.bot)

    @discord.ui.button(label="Straight", custom_id="straight", style=discord.ButtonStyle.blurple)
    async def straight(self, interaction, button):
        await self.applyRole(interaction, "straight")
    
    @discord.ui.button(label="Gay", custom_id="gay", style=discord.ButtonStyle.blurple)
    async def gay(self, interaction, button):
        await self.applyRole(interaction, "gay")
    
    @discord.ui.button(label="Lesbian", custom_id="lesbian", style=discord.ButtonStyle.blurple)
    async def lesbain(self, interaction, button):
        await self.applyRole(interaction, "lesbian")
    
    @discord.ui.button(label="Bisexual", custom_id="bisexual", style=discord.ButtonStyle.blurple)
    async def bisexual(self, interaction, button):
        await self.applyRole(interaction, "bisexual")
    
    @discord.ui.button(label="Pansexual", custom_id="pansexual", style=discord.ButtonStyle.blurple)
    async def pansexual(self, interaction, button):
        await self.applyRole(interaction, "pansexual")
    
    @discord.ui.button(label="Asexual", custom_id="asexual", style=discord.ButtonStyle.blurple)
    async def asexual(self, interaction, button):
        await self.applyRole(interaction, "asexual")

class GenderRoles(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    def getGenderDB(self):
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        db = client[database]
        collection = getSetting(os.getenv("SETTINGS_reactionRolesCollection"))
        rrCollection = db[collection]
        result = rrCollection.find_one("genderRoles")
        if result == None:
            logging.info(' result = rrCollection.find_one("genderRoles") >> result == None!')
            sys.exit()
        payload = result["value"]
        return payload
    
    async def applyRole(self, interaction:discord.Interaction, role:str):
        targetRoleID = int(self.getGenderDB()[role])
        guild = interaction.guild
        if guild == None:
            logging.info(f"Error: RR03-0 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR03-0 - {role}")
            sys.exit()
        targetRole = guild.get_role(targetRoleID)
        if targetRole == None:
            logging.info(f"Error: RR03-1 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR03-1 - {role}")
            sys.exit()
        user = interaction.user
        if type(user) is not discord.Member:
            logging.info(f"Error: RR03-2 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR03-2 - {role}")
            sys.exit()
        if targetRole in user.roles:
            await user.remove_roles(targetRole)
            await interaction.response.send_message(f"Removed the role `{targetRole.name}` from {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Removed {targetRole.name} Role", interaction.channel, self.bot)
        else:
            await user.add_roles(targetRole)
            await interaction.response.send_message(f"Added the role `{targetRole.name}` to {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Added {targetRole.name} Role", interaction.channel, self.bot)

    @discord.ui.button(label="Male", custom_id="male", style=discord.ButtonStyle.blurple)
    async def male(self, interaction, button):
        await self.applyRole(interaction, "male")
    
    @discord.ui.button(label="Female", custom_id="female", style=discord.ButtonStyle.blurple)
    async def female(self, interaction, button):
        await self.applyRole(interaction, "female")
    
    @discord.ui.button(label="Non-binary", custom_id="nb", style=discord.ButtonStyle.blurple)
    async def nonbinary(self, interaction, button):
        await self.applyRole(interaction, "nonbinary")

class PronounRoles(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    def getGenderDB(self):
        from pymongo import MongoClient
        CONNECTION_STRING = os.getenv("MONGO_connection_string")
        client: MongoClient = MongoClient(CONNECTION_STRING)
        database = os.getenv("MONGO_maindb")
        if database == None:
            logging.info("BAD ENV MONGO_maindb")
            sys.exit()
        db = client[database]
        collection = getSetting(os.getenv("SETTINGS_reactionRolesCollection"))
        rrCollection = db[collection]
        result = rrCollection.find_one("pronounRoles")
        if result == None:
            logging.info(' result = rrCollection.find_one("pronounRoles") >> result == None!')
            sys.exit()
        payload = result["value"]
        return payload
    
    async def applyRole(self, interaction:discord.Interaction, role:str):
        targetRoleID = int(self.getGenderDB()[role])
        guild = interaction.guild
        if guild == None:
            logging.info(f"Error: RR04-0 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR04-0 - {role}")
            sys.exit()
        targetRole = guild.get_role(targetRoleID)
        if targetRole == None:
            logging.info(f"Error: RR04-1 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR04-1 - {role}")
            sys.exit()
        user = interaction.user
        if type(user) is not discord.Member:
            logging.info(f"Error: RR04-2 - {role}")
            await interaction.response.send_message(f"Internal Error, Please report this. | RR04-2 - {role}")
            sys.exit()
        if targetRole in user.roles:
            await user.remove_roles(targetRole)
            await interaction.response.send_message(f"Removed the role `{targetRole.name}` from {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Removed {targetRole.name} Role", interaction.channel, self.bot)
        else:
            await user.add_roles(targetRole)
            await interaction.response.send_message(f"Added the role `{targetRole.name}` to {user.mention}", ephemeral=True)
            await userCommandLogs(user, f"Used Button > {targetRole.name} REACTION ROLE > Added {targetRole.name} Role", interaction.channel, self.bot)

    @discord.ui.button(label="He/Him", custom_id="he", style=discord.ButtonStyle.blurple)
    async def he(self, interaction, button):
        await self.applyRole(interaction, "he")
    
    @discord.ui.button(label="She/Her", custom_id="she", style=discord.ButtonStyle.blurple)
    async def she(self, interaction, button):
        await self.applyRole(interaction, "she")
    
    @discord.ui.button(label="They/Them", custom_id="they", style=discord.ButtonStyle.blurple)
    async def they(self, interaction, button):
        await self.applyRole(interaction, "they")
    
    @discord.ui.button(label="Other Pronouns", custom_id="other", style=discord.ButtonStyle.blurple)
    async def other(self, interaction, button):
        await self.applyRole(interaction, "other")
    

def init(bot:commands.Bot):
    bot.add_view(SpeciesRoles(bot))
    bot.add_view(ColorRoles(bot))
    bot.add_view(SORoles(bot))
    bot.add_view(GenderRoles(bot))
    bot.add_view(PronounRoles(bot))
    logging.info("Init of Reaction Role Classes Complete!")
