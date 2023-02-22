from discord.ext import commands
import time
import discord
import logging


class Listeners(commands.Cog, name="On Event Listeners"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        from modules.messageLogger.onMessageDelete import onMessageDelete
        await onMessageDelete(message, self.bot)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        from modules.messageLogger.onMessageEdit import onMessageEdit
        await onMessageEdit(message_before, message_after, self.bot)

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if self.bot.user.mentioned_in(message) and message.author != self.bot.user: #type:ignore
            if "@everyone" not in message.content and "@here" not in message.content:
                await message.reply(f"Greetings {message.author.mention}!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        from modules.logging.userActions import onJoin
        await onJoin(member, self.bot)

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload):
        from modules.logging.userActions import onLeaveRaw
        await onLeaveRaw(payload, self.bot)

    @commands.Cog.listener()
    async def on_ready(self):
        from modules.utilities.reactionRolesClasses import init as ReactionRolesInit
        from modules.utilities.modTickets import ModTicket
        from modules.utilities.verification import verificationClass
        logging.info("Starting up...")

        ReactionRolesInit(self.bot)
        self.bot.add_view(verificationClass(self.bot))
        self.bot.add_view(ModTicket(self.bot))

        from modules.utilities.verification import verificationNotify
        verificationNotify(self.bot) # INIT THE VERIFICATION NOTIFIER

        with open('./database/uptime.db', 'w') as fp:
            fp.write(str(time.time()))

        logging.info("Ready!")

async def setup(bot:commands.Bot):
    logging.info(f"{__file__} - Setting up...")
    await bot.add_cog(
        Listeners(bot)
    )
    logging.info(f"{__file__} - Done!")