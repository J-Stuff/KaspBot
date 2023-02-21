from discord.ext import commands
import logging
import sys
cogs = ['cogs.AdminCommands', 'cogs.Commands', 'cogs.LoopingFunctions', 'cogs.OnEvent']






class cogController():
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot

    def getOnlineCogs(self):
        with open("./database/cogs.db", 'r') as fp:
            cogs = fp.read().splitlines()
        return cogs
    
    def addCog(self, cog:str):
        online = self.getOnlineCogs()
        if cog in online:
            return False
        
        with open("./database/cogs.db", 'a') as fp:
            fp.write(cog)
            fp.write('\n')
        return True
    
    def removeCogs(self):
        open("./database/cogs.db", 'w').close()
        return True
    

    async def reloadCogs(self):
        if not self.removeCogs():
            logging.fatal("Cog Reload Database Failure! -- Stopping to prevent database damage!")
            logging.info("Cog Reload Database Failure! -- Stopping to prevent database damage!")
            sys.exit("Cog Reload Database Failure! -- Stopping to prevent database damage!")
        for cog in cogs:
            logging.info(f"Reloading cog/extension: {cog}")
            try:
                await self.bot.reload_extension(cog)
            except (commands.ExtensionNotFound, commands.NoEntryPointError, commands.ExtensionFailed, commands.ExtensionNotFound) as e:
                logging.fatal(f"Failed to load cog/extension: {cog} -- {e}")
                logging.info(f"Failed to load cog/extension: {cog} -- {e}")
                sys.exit(f"Failed to load cog/extension: {cog} -- {e}")
            
            if not self.addCog(cog):
                logging.fatal("Cog Reload Database Failure! -- Stopping to prevent database damage!")
                logging.info("Cog Reload Database Failure! -- Stopping to prevent database damage!")
                sys.exit("Cog Reload Database Failure! -- Stopping to prevent database damage!")
                
            logging.info(f"Reloaded cog/extension: {cog}")

    async def initCogs(self):
        for cog in cogs:
            logging.info(f"Loading cog/extension: {cog}")
            if not self.addCog(cog):
                logging.fatal("Cog Load Database Failure! -- Stopping to prevent database damage!")
                logging.info("Cog Load Database Failure! -- Stopping to prevent database damage!")
                sys.exit("Cog Load Database Failure! -- Stopping to prevent database damage!")
            try:
                await self.bot.load_extension(cog)
            except (commands.ExtensionNotFound, commands.NoEntryPointError, commands.ExtensionFailed) as e:
                logging.fatal(f"Failed to load cog/extension: {cog} -- {e}")
                logging.info(f"Failed to load cog/extension: {cog} -- {e}")
                sys.exit(f"Failed to load cog/extension: {cog} -- {e}")

            logging.info(f"Loaded cog/extension: {cog}")