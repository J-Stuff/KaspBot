from modules.logging.adminCommandLogs import adminCommandLogs

async def channelUnMute(interaction, user, bot):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    await interaction.channel.set_permissions(user, overwrite=None)
    await interaction.response.send_message(f"Done, removed the channel mute for <@{user.id}>!")
    await adminCommandLogs(interaction.user, f"/channel-unmute for {user}", interaction.channel.id, bot)

async def channelMute(interaction, user, reason, bot):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    if interaction.user.id == user.id:
        interaction.response.send_message("You can't mute yourself stupid (the dev learnt this one the hard way :/)", ephemeral=True)
        return
    await interaction.channel.set_permissions(user, add_reactions=False, send_messages=False)
    await interaction.response.send_message(f"Done, channel muted <@{user.id}>!\nReason: `{reason}`")
    await adminCommandLogs(interaction.user, f"/channel-mute {user} | {reason}", interaction.channel.id, bot)