import os
from _kaspBot import KaspBot

try:
    token = os.environ['BOT_TOKEN']
except KeyError:
    print('No token found. Ensure that the BOT_TOKEN environment variable is set.')
    exit(1)


bot = KaspBot()

if __name__ == '__main__':
    bot.run(token)
else:
    print('This file is not meant to be imported.')
    exit(1)


# Run KaspBot from here