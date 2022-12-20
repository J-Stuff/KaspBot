import discord
from modules.logging.userCommandLogs import userCommandLogs
from modules.config.loadConfigs import botConfig

class SpeciesRoles(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Canine", custom_id="Canine", style=discord.ButtonStyle.gray,)
    async def button0(self, interaction, button):
        role = int(botConfig()["species_roles"]["canine"])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Feline", custom_id="Feline", style=discord.ButtonStyle.gray,)
    async def button1(self, interaction, button):
        role = int(botConfig()["species_roles"]["feline"])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Mustelid", custom_id="Mustelid", style=discord.ButtonStyle.gray,)
    async def button2(self, interaction, button):
        role = int(botConfig()["species_roles"]['mustelid'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Hybrid", custom_id="Hybrid", style=discord.ButtonStyle.gray,)
    async def button3(self, interaction, button):
        role = int(botConfig()["species_roles"]['hybrid'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)


class ColorRoles(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Red", custom_id="Red", style=discord.ButtonStyle.gray,)
    async def button0(self, interaction, button):
        role = int(botConfig()["color_roles"]['red'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Orange", custom_id="Orange", style=discord.ButtonStyle.gray,)
    async def button1(self, interaction, button):
        role = int(botConfig()["color_roles"]['orange'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Yellow", custom_id="Yellow", style=discord.ButtonStyle.gray,)
    async def button2(self, interaction, button):
        role = int(botConfig()["color_roles"]['yellow'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Green", custom_id="Green", style=discord.ButtonStyle.gray,)
    async def button3(self, interaction, button):
        role = int(botConfig()["color_roles"]['green'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Teal", custom_id="Teal", style=discord.ButtonStyle.gray,)
    async def button4(self, interaction, button):
        role = int(botConfig()["color_roles"]['teal'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Cyan", custom_id="Cyan", style=discord.ButtonStyle.gray,)
    async def button5(self, interaction, button):
        role = int(botConfig()["color_roles"]['cyan'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Blue", custom_id="Blue", style=discord.ButtonStyle.gray,)
    async def button6(self, interaction, button):
        role = int(botConfig()["color_roles"]['blue'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Purple", custom_id="Purple", style=discord.ButtonStyle.gray,)
    async def button7(self, interaction, button):
        role = int(botConfig()["color_roles"]['purple'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Pink", custom_id="Pink", style=discord.ButtonStyle.gray,)
    async def button8(self, interaction, button):
        role = int(botConfig()["color_roles"]['pink'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)


class SORoles(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Straight", custom_id="Straight", style=discord.ButtonStyle.gray, emoji="<:hetro_flag:1038705337865342976>")
    async def button0(self, interaction, button):
        role = int(botConfig()["so_roles"]['straight'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Gay", custom_id="Gay", style=discord.ButtonStyle.gray, emoji="<:queer_flag:1038707440692232292>")
    async def button1(self, interaction, button):
        role = int(botConfig()["so_roles"]['gay'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Lesbian", custom_id="Lesbian", style=discord.ButtonStyle.gray, emoji="<:lesbian_flag:1038705904402583612>")
    async def button2(self, interaction, button):
        role = int(botConfig()["so_roles"]['lesbian'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Bisexual", custom_id="Bisexual", style=discord.ButtonStyle.gray, emoji="<:bisexual_flag:1038706509833588826>")
    async def button3(self, interaction, button):
        role = int(botConfig()["so_roles"]['bisexual'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Pansexual", custom_id="Pansexual", style=discord.ButtonStyle.gray, emoji="<:pansexual_flag:1038706723529162782>")
    async def button4(self, interaction, button):
        role = int(botConfig()["so_roles"]['pansexual'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

    @discord.ui.button(label="Asexual", custom_id="Asexual", style=discord.ButtonStyle.gray, emoji="<:asexual_flag:1038706919231205406>")
    async def button5(self, interaction, button):
        role = int(botConfig()["so_roles"]['asexual'])
        user = interaction.user
        if role in [y.id for y in user.roles]:
            await user.remove_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have removed the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Remove role {user.guild.get_role(role)}", interaction.channel.id, self.bot)

        else:
            await user.add_roles(user.guild.get_role(role))
            await interaction.response.send_message(f"You have added the role {user.guild.get_role(role)}", ephemeral=True)
            await userCommandLogs(interaction.user, f"BUTTON: Add role {user.guild.get_role(role)}", interaction.channel.id, self.bot)