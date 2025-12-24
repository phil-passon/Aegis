import discord
from discord.ext import commands
from discord import app_commands, ui
import asyncio
import random

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

    @ui.button(label="Ask the Intern", style=discord.ButtonStyle.primary, emoji="☕", custom_id="sassy_intern_button")
    async def intern_button(self, interaction: discord.Interaction, button: ui.Button):
        responses = [
            "I've analyzed your problem. It seems to be a 'User Error'.",
            "Have you tried turning your router off and leaving it off? Forever?",
            "I'd help you, but I'm currently on my 15th coffee break of the hour.",
            "I'm just an intern. I don't even get paid in Discord Nitro for this.",
            "That sounds like a 'next year' problem to me.",
            "Error 404: Intern's motivation not found.",
            "Have you tried asking nicely? Computers have feelings too, you know.",
            "I'm currently busy googling how to do my own job. Please hold.",
            "I'll get right on that... as soon as I finish this 4-hour lunch break.",
            "My supervisor said I should help you, but they aren't looking right now.",
            "I've put your issue in the 'Important' folder. (It's actually the trash can).",
            "Have you tried clicking it harder? Sometimes that works.",
            "I'm not saying it's your fault, but it's definitely not my fault.",
            "I'd escalate this, but the stairs are broken and I don't do elevators.",
            "Is this a 'now' thing or can it wait until I've retired?",
            "I've consulted the spirits. They said 'ask again when you have snacks'.",
            "I was going to help, but then I saw a very interesting bird outside.",
            "Have you considered that maybe the universe just wants you to fail?"
        ]

        embed = discord.Embed(
            title="☕ The Intern's Professional™ Advice",
            description=random.choice(responses),
            color=discord.Color.blurple()
        )
        embed.set_footer(text="Warning: Intern is currently unpaid and unmotivated.")

        await interaction.response.send_message(embed=embed)


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