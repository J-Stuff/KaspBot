import discord
from discord.ext import commands
from modules.logging.adminCommandLogs import adminCommandLogs
async def warn(interaction:discord.Interaction, target:discord.Member, reason:str, bot:commands.Bot):
    if not interaction.user.guild_permissions.ban_members: #type:ignore
        await interaction.response.send_message("You do not have permission to run this!", ephemeral=True)
        return
    
    await interaction.response.defer(thinking=True, ephemeral=True)

    user_warnEmbed = discord.Embed(title='You have received a Warn!', description=f"You recieved a warn from {interaction.guild.name}") #type:ignore
    user_warnEmbed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) #type:ignore
    user_warnEmbed.add_field(name="Reason", value=reason)

    try:
        await target.send(embed=user_warnEmbed)
    except discord.Forbidden:
        await interaction.followup.send("This user either has blocked me, or has their DM's disabled for this server!\nI cannot send a message to them.", ephemeral=True)
    except:
        await interaction.followup.send("This user either has blocked me, or has their DM's disabled for this server!", ephemeral=True)
    else:
        await interaction.followup.send("Done!, I sent the user the following message:", embed=user_warnEmbed, ephemeral=True)
        await adminCommandLogs(interaction.user, f"Warned User: {target}, for {reason}", interaction.channel, bot)
        