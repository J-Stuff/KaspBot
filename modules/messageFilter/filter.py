def addFilter(phrase: str):
    with open('./modules/messageFilter/blacklist.database.bin', 'a') as fp:
        fp.write(str(phrase.lower()))
        fp.write('\n')
    
def getWlChannels():
    with open('./modules/messageFilter/whitelisted_channels.database.bin', 'r') as fp:
        whitelist = fp.read().splitlines()
    return whitelist
        
def getFilter():
    with open('./modules/messageFilter/blacklist.database.bin', 'r') as fp:
        blacklist = fp.read().splitlines()
    return blacklist

def removeFilter(phrase: str):
    phrase = phrase.lower()
    with open('./modules/messageFilter/blacklist.database.bin', 'r+') as fp:
        blacklist = fp.read().splitlines()
    try:
        blacklist.remove(phrase)
    except ValueError:
        return False
    else:
        payload = ""
        for line in blacklist:
            payload+=str(line)
            payload+='\n'
        with open('./modules/messageFilter/blacklist.database.bin', 'w') as fp:
            fp.write(payload)
        return True
