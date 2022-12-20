from modules.config.loadConfigs import botConfig

def debugLog(message):
    if botConfig()["debug"]:
        print(message)