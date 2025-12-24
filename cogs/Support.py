import discord
from discord.ext import commands
from discord import app_commands, ui
import asyncio

from Main import NAME, BOT_INVITE, ICON_URL, EMBED_COLOUR, SOURCE_CODE, STAFF_ROLE_NAME


class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_ticket_button")
    async def close_button(self, interaction: discord.Interaction, button: ui.Button):
        is_staff = interaction.user.guild_permissions.manage_channels
        if is_staff or interaction.channel.permissions_for(interaction.user).send_messages:
            await interaction.response.send_message("Closing ticket in 5 seconds...")
            await asyncio.sleep(5)
            await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")
        else:
            await interaction.response.send_message("❌ You do not have permission to close this ticket.",
                                                    ephemeral=True)


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(TicketView())

    @app_commands.command(name="ticket", description="Open a private support ticket.")
    async def ticket(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, name="Tickets")
        if category is None:
            category = await guild.create_category("Tickets")

        # --- IMPROVED CHECK: Search by User ID in the Topic ---
        for channel in category.text_channels:
            if channel.topic == f"Ticket Owner ID: {user.id}":
                return await interaction.response.send_message(
                    f"❌ You already have an open ticket: {channel.mention}",
                    ephemeral=True
                )

        staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category,
            overwrites=overwrites,
            topic=f"Ticket Owner ID: {user.id}",
            reason=f"Ticket created by {user.name}"
        )

        embed = discord.Embed(
            title="🎫 Support Ticket",
            description=f"Hi {user.mention}, staff will be with you shortly.\nClick the button below to close this session.",
            colour=EMBED_COLOUR
        )

        await ticket_channel.send(embed=embed, view=TicketView())
        await interaction.response.send_message(f"✅ Created: {ticket_channel.mention}", ephemeral=True)

    @app_commands.command(name="close", description="Closes and deletes the current support ticket.")
    async def close(self, interaction: discord.Interaction):
        if not (interaction.channel.category and interaction.channel.category.name == "Tickets"):
            return await interaction.response.send_message("❌ This is not a ticket channel.", ephemeral=True)

        is_staff = interaction.user.guild_permissions.manage_channels

        if is_staff or interaction.channel.permissions_for(interaction.user).send_messages:
            await interaction.response.send_message("Closing ticket in 5 seconds...")
            await asyncio.sleep(5)
            await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}.")
        else:
            await interaction.response.send_message("❌ You do not have permission to close this ticket.",
                                                    ephemeral=True)


async def setup(bot):
    await bot.add_cog(Support(bot))