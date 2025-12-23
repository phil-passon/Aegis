import discord
from discord.ext import commands
from discord import app_commands

from Main import NAME, BOT_INVITE, ICON_URL, EMBED_COLOUR, SOURCE_CODE, STAFF_ROLE_NAME


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket", description="Open a private support ticket to speak with staff.")
    async def ticket(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, name="Tickets")
        if category is None:
            category = await guild.create_category("Tickets")

        staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel_name = f"ticket-{user.name}"
        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            reason=f"Ticket created by {user.name}"
        )

        embed = discord.Embed(
            title="🎫 Support Ticket",
            description=f"Hi {user.mention}, thank you for reaching out.\nStaff will be with you shortly. Use `/close` to end this session.",
            colour=EMBED_COLOUR
        )
        await ticket_channel.send(embed=embed)

        await interaction.response.send_message(f"✅ Your ticket has been created: {ticket_channel.mention}",
                                                ephemeral=True)

    @app_commands.command(name="close", description="Closes and deletes the current support ticket.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def close(self, interaction: discord.Interaction):
        if interaction.channel.category and interaction.channel.category.name == "Tickets":
            await interaction.response.send_message("Closing ticket in 5 seconds...")
            import asyncio
            await asyncio.sleep(5)
            await interaction.channel.delete(reason="Ticket closed by staff/user.")
        else:
            await interaction.response.send_message("❌ This command can only be used inside a ticket channel.",
                                                    ephemeral=True)


async def setup(bot):
    await bot.add_cog(Support(bot))