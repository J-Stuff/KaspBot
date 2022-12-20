import time
import tinydb
import random
import discord
from discord.utils import get
from modules.config.loadConfigs import botConfig



async def muteUser(interaction, target, mute_reason, mute_duration, bot):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    if interaction.user.id == target.id:
        interaction.response.send_message("You can't mute yourself stupid (the dev learnt this one the hard way :/)", ephemeral=True)
        return
    unix = int(time.time())


    mute_db = tinydb.TinyDB('./data/mutes.database.json')
    
    if mute_duration == '10 minutes':
        end_unix = unix +600
    elif mute_duration == '1 hour':
        end_unix = unix +3600
    elif mute_duration == '3 hours':
        end_unix = unix +10800
    elif mute_duration == '6 hours':
        end_unix = unix +21600
    elif mute_duration == '12 hours':
        end_unix = unix +43200
    elif mute_duration == '1 day':
        end_unix = unix +86400
    elif mute_duration == '3 days':
        end_unix = unix +259200
    elif mute_duration == '3 days':
        end_unix = unix +604800
    elif mute_duration == 'permanently':
        end_unix = 9999999999 # Mutes user until Sat Nov 20 2286 17:46:39 GMT+0000 :troll:
    else:
        return
    
    mute_db.insert({"mute_id": str(unix) + str(random.randint(0, 9)), "user_id": target.id, "admin_id": interaction.user.id, "mute_reason": mute_reason, "mute_applied": unix, "mute_expires": end_unix, "mute_active": True})
    mute_db.close()
    muteObj = get(interaction.guild.roles, id=botConfig()["mutedRole"])
    await target.add_roles(muteObj) # type: ignore
    embed = discord.Embed(title=f"Your have been muted in {interaction.guild.name}", color=discord.colour.parse_hex_number("e32dd4"))
    embed.set_author(name="Mute Manager")
    embed.add_field(name="Mute Reason:", value=mute_reason)
    if end_unix != 9999999999:
        expire_message = f"Your mute will expire <t:{end_unix}:R>"
    else:
        expire_message = "This mute is permanent, and will not expire automatically!"
    embed.add_field(name="Expires:", value=expire_message)
    await target.send(embed=embed)
    await interaction.response.send_message(f"Done! Muted <@{target.id}> until <t:{end_unix}:F> > <t:{end_unix}:R>", ephemeral=True)