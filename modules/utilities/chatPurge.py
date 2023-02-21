from modules.logging.adminCommandLogs import adminCommandLogs

async def chatPurge(interaction, count, bot):
    count += 1
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=False, thinking=False)
    await interaction.channel.purge(limit=count)
    await interaction.channel.send(f"Done! Purged `{count}` messages!")
    await adminCommandLogs(interaction.user, f"Purged {count} messages!", interaction.channel, bot)