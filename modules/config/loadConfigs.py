import json
def botJson():
    with open('./config/bot.json', 'r') as fp:
        botJson = json.loads(fp.read())
    return botJson

def botConfig():
    with open('./config/config.json', 'r') as fp:
        botConfig = json.loads(fp.read())
    return botConfig