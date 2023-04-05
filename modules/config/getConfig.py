import json
import logging
logger = logging.getLogger('kaspbot')


class settings():
    def readSettings(self):
        with open('./config/config.json', 'r') as fp:
            x = json.load(fp)
            fp.close()
        return x


    def getReactionRoleID(self, type:str, key:str):
        logger.debug(f"getReactionRoleID > Looking for [{type}] [{key}]")
        config:dict = self.readSettings()
        try:
            id = config["reactionRoles"][type][key]
        except:
            raise Exception(f"Cannot find [{type}] [{key}] in the config!")
        logger.debug(f"getReactionRoleID > {id}")
        return int(id)
    
    def getChannelID(self, key:str):
        logger.debug(f"getChannelID > Looking for [channelIds] [{key}]")
        config:dict = self.readSettings()
        try:
            id = config["channelIds"][key]
        except:
            raise Exception(f"Cannot find [channelIds] [{key}] in the config!")
        logger.debug(f"getChannelID > {id}")
        return id
    
    def getMiscId(self, key:str) -> int:
        logger.debug(f"getMiscId > Looking for [miscIds] [{key}]")
        config:dict = self.readSettings()
        try:
            id = config["miscIds"][key]
        except:
            raise Exception(f"Cannot find [miscIds] [{key}] in the config!")
        logger.debug(f"getMiscId > {id}")
        return id
    
    def getBotSetting(self, key:str) -> str:
        config:dict = self.readSettings()
        try:
            setting = config["botSettings"][key]
        except:
            raise Exception(f"Cannot find [miscIds] [{key}] in the config!")
        return setting
    
    