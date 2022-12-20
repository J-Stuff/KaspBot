import discord
import tinydb
import time
from modules.config.loadConfigs import botConfig
from modules.logging.adminCommandLogsMessage import adminCommandLogsMessage

async def muteMaintenance(bot):
    # print("Running mute maintenance...")
    
    import time

    async def unmute(userID):
        guild = await bot.fetch_guild(botConfig()["guild"]) # type: ignore
        user = await guild.fetch_member(int(userID))
        guild = bot.get_guild(botConfig()["guild"])
        muteRole = guild.get_role(botConfig()["mutedRole"]) # type: ignore
        await user.remove_roles(muteRole) # type: ignore


    mute_db = tinydb.TinyDB("./data/mutes.database.json")

    # {"mute_id": str(unix) + str(random.randint(0, 9)), "user_id": target.id, "admin_id": interaction.user.id, "mute_reason": mute_reason, "mute_applied": unix, "mute_expires": end_unix, "mute_active": True}

    Mutes = tinydb.Query()
    result = mute_db.search(Mutes.mute_active == True) # type:ignore

    for activeMute in result:  # type: ignore
        # print(activeMute)
        unix = int(time.time())
        if int(activeMute["mute_expires"]) < int(unix):
            await unmute(activeMute["user_id"])
            mute_db.update({"mute_active": False}, Mutes.mute_id == activeMute["mute_id"]) # type:ignore
            mute_db.close()
            guild = await bot.fetch_guild(botConfig()["guild"]) # type: ignore
            user = await guild.fetch_member(int(activeMute["user_id"]))
            await adminCommandLogsMessage(user, "MuteManager: Temp-Mute Expired", bot)
            embed = discord.Embed(title="Your mute has expired!",
                                    description=f"Your mute in `{guild.name}` has expired", color=discord.colour.parse_hex_number("3c00f8"))
            embed.set_author(name="Mute Manager")
            embed.add_field(name="Mute Reason:",
                            value=activeMute["mute_reason"])
            await user.send(embed=embed)