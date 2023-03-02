import json
import logging


class settings():
    def readSettings(self):
        logging.debug("Reading config file...")
        with open('./config/config.json', 'r') as fp:
            x = json.load(fp)
            fp.close()
        logging.debug(x)
        return x


    def getReactionRoleID(self, type:str, key:str):
        logging.debug(f"getReactionRoleID > Looking for [{type}] [{key}]")
        config:dict = self.readSettings()
        try:
            id = config["reactionRoles"][type][key]
        except:
            raise Exception(f"Cannot find [{type}] [{key}] in the config!")
        logging.debug(f"getReactionRoleID > {id}")
        return int(id)
    
    def getBotVersion(self):
        logging.debug(f"getBotVersion > Looking for bot version")
        config:dict = self.readSettings()
        try:
            version:str = config["botSettings"]["botVersion"]
        except:
            raise Exception(f"Cannot find [botSettings] [botVersion] in the config!")
        logging.debug(f"getBotVersion > {version}")
        return version
    
    def getChannelID(self, key:str):
        logging.debug(f"getChannelID > Looking for [channelIds] [{key}]")
        config:dict = self.readSettings()
        try:
            id = config["channelIds"][key]
        except:
            raise Exception(f"Cannot find [channelIds] [{key}] in the config!")
        logging.debug(f"getChannelID > {id}")
        return id
    
    def getMiscId(self, key:str):
        logging.debug(f"getMiscId > Looking for [miscIds] [{key}]")
        config:dict = self.readSettings()
        try:
            id = config["miscIds"][key]
        except:
            raise Exception(f"Cannot find [miscIds] [{key}] in the config!")
        logging.debug(f"getMiscId > {id}")
        return id
    
    