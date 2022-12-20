import discord
import time
import random
from discord.utils import get
from discord.ext import commands
from modules.logging.adminCommandLogs import adminCommandLogs
from modules.config.loadConfigs import botConfig


async def user_verf(interaction, target: discord.Member, bot):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return

    async def giveVerRole(interaction):
        role = target.guild.get_role(botConfig()["baseRole"])
        updatedTarget = get(interaction.guild.members, id=target.id)
        if role in updatedTarget.roles:  # type: ignore
            await interaction.response.send_message(f"User is already verified!", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=False, thinking=True)
        embedLoad = discord.Embed(
            title="Verification", color=discord.colour.parse_hex_number("ffcc00"))
        embedLoad.add_field(
            name="Adding Roles", value="<a:loader2:1041678096228691980> Please wait...")
        loader = await interaction.followup.send(embed=embedLoad, ephemeral=False)
        guild = bot.get_guild(botConfig()["guild"])
        unv_role = guild.get_role(botConfig()["unverifiedRoleId"])
        ver_role = guild.get_role(botConfig()["baseRole"])
        await target.add_roles(ver_role)
        await target.remove_roles(unv_role)
        await adminCommandLogs(interaction.user, f"/verify\nVerified <@{target.id}> (`{target}` // `{target.id}`)!", interaction.channel.id, bot)
        try:
            await target.send(f"Your verification request in {target.guild.name} was accepted. Welcome!")
        except:
            pass
        embedDone = discord.Embed(
            title="Verification", color=discord.colour.parse_hex_number("289100"))
        embedDone.add_field(name="Verification Complete",
                            value=f"Welcome, <@{target.id}>!")
        embedDone.set_author(name=interaction.user,
                             icon_url=interaction.user.avatar)
        time.sleep(random.randint(1, 5))
        await interaction.followup.edit_message(message_id=loader.id, embed=embedDone)

    embed = discord.Embed(title="Verification Interface",
                          description=f"Information about: {target}")
    accountCreation = target.created_at
    accountUnix = int(time.mktime(accountCreation.timetuple()))
    embed.add_field(name="Account Created",
                    value=f"<t:{accountUnix}:F>\nWhich was: <t:{accountUnix}:R>", inline=False)
    embed.add_field(
        name='To cancel', value="To cancel this operation, simply ignore this embed and hit 'dismiss message' below", inline=False)
    verifyButton = discord.ui.Button(
        label="Verify User", style=discord.ButtonStyle.green)

    verifyButton.callback = giveVerRole

    view = discord.ui.View()
    view.add_item(verifyButton)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def unv_scan(interaction, bot: commands.Bot):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(f"You don't have permissions to do that!", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=False, thinking=True)
    members = interaction.guild.members

    description = ""
    noRoleMembers = []
    for member in members:
        member: discord.Member
        if len(member.roles) == 1:
            guild = bot.get_guild(botConfig()["guild"])
            unv_role = guild.get_role( # type:ignore
                botConfig()["unverifiedRoleId"])  
            await member.add_roles(unv_role)  # type:ignore

    members = interaction.guild.members
    for member in members:
        member: discord.Member
        for role in member.roles:
            if role.id == botConfig()["unverifiedRoleId"]:
                noRoleMembers.append(member.id)

    for user in noRoleMembers:
        target = get(interaction.guild.members, id=user)
        joined = target.joined_at.strftime('%s')  # type: ignore
        description += f"<@{user}> > Joined server on: <t:{joined}:F>\n"
    embed = discord.Embed(title="Users not currently verified:", description=description,
                          color=discord.colour.parse_hex_number("ff00ff"))
    await interaction.followup.send(embed=embed)
    await adminCommandLogs(interaction.user, f"/unverified-scan", interaction.channel.id, bot)
