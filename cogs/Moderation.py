import discord
from discord.ext import commands
from discord import app_commands

from Main import NAME, BOT_INVITE, ICON_URL, EMBED_COLOUR, SOURCE_CODE, STAFF_ROLE_NAME


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -----------------------------------Slash Command Checks--------------------------------------#

    @staticmethod
    def is_staff_perms():
        async def predicate(interaction: discord.Interaction) -> bool:
            if discord.utils.get(interaction.user.roles, name=STAFF_ROLE_NAME):
                return True
            else:
                error_embed = discord.Embed(
                    colour=discord.Colour.red(),
                    title="__**Error**__",
                    description=f"You don't have the required ``{STAFF_ROLE_NAME}`` role to use this command."
                )
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
                return False

        return app_commands.check(predicate)

    # -----------------------------------Moderation Commands--------------------------------------#

    @app_commands.command(name="embed", description="Generates a simple embed from your text.")
    @is_staff_perms()
    @app_commands.describe(message="The text content for the embed description.")
    async def embed_slash(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message("Sending embed...", ephemeral=True, delete_after=3)
        embed = discord.Embed(colour=EMBED_COLOUR, description=message)
        embed.add_field(name="\u200b", value=f"[Invite]({BOT_INVITE})")
        await interaction.channel.send(embed=embed)

    @app_commands.command(name="kick", description="Kicks a member from the server.")
    @is_staff_perms()
    @app_commands.default_permissions(kick_members=True)
    @app_commands.describe(member="The member to kick.", reason="The reason for the kick.")
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            desc = "You cannot kick a member with an equal or higher role than you."
        elif member.top_role >= interaction.guild.me.top_role:
            desc = f"I cannot kick {member.display_name} as their highest role is equal to or higher than my own."
        else:
            await member.kick(reason=reason)
            embed = discord.Embed(colour=EMBED_COLOUR, title='__**Kicked**__',
                                  description=f'**Member**:{member.mention}\n**Reason**: {reason or "No reason provided"}')
            await interaction.response.send_message(embed=embed)
            return

        err_embed = discord.Embed(colour=discord.Colour.red(), title="__**Error**__", description=desc)
        await interaction.response.send_message(embed=err_embed, ephemeral=True)

    @app_commands.command(name="ban", description="Bans a member from the server.")
    @is_staff_perms()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban.", reason="The reason for the ban.")
    async def ban_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role:
            desc = "You cannot ban a member with an equal or higher role than you."
        elif member.top_role >= interaction.guild.me.top_role:
            desc = f"I cannot ban {member.display_name} as their highest role is equal to or higher than my own."
        else:
            await member.ban(reason=reason)
            embed = discord.Embed(colour=EMBED_COLOUR, title='__**Banned**__',
                                  description=f'**Member:**{member.mention}\n**Reason:** {reason or "No reason provided"}')
            await interaction.response.send_message(embed=embed)
            return

        err_embed = discord.Embed(colour=discord.Colour.red(), title="__**Error**__", description=desc)
        await interaction.response.send_message(embed=err_embed, ephemeral=True)

    @app_commands.command(name="unban", description="Unbans a user using their ID.")
    @is_staff_perms()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.describe(user_id="The ID of the user to unban.", reason="The reason for the unban.")
    async def unban_slash(self, interaction: discord.Interaction, user_id: str, reason: str = None):
        try:
            target_id = int(user_id)
            banned_users = [entry async for entry in interaction.guild.bans()]
            unban_entry = discord.utils.find(lambda entry: entry.user.id == target_id, banned_users)

            if not unban_entry:
                err_embed = discord.Embed(colour=discord.Colour.orange(), title="__**Unban Error**__",
                                          description=f"User with ID **{user_id}** is not currently banned.")
                return await interaction.response.send_message(embed=err_embed, ephemeral=True)

            await interaction.guild.unban(unban_entry.user, reason=reason)
            embed = discord.Embed(colour=discord.Colour.green(), title='__**Unbanned**__',
                                  description=f'**User:** {unban_entry.user.name}\n**Reason:** {reason or "No reason provided"}')
            await interaction.response.send_message(embed=embed)

        except ValueError:
            await interaction.response.send_message("Invalid User ID format.", ephemeral=True)

    @app_commands.command(name="clear", description="Bulk deletes messages in the current channel.")
    @is_staff_perms()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(amount="The number of messages to delete (1-100).")
    async def clear_slash(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        await interaction.response.defer(ephemeral=True)
        try:
            deleted = await interaction.channel.purge(limit=amount)
            embed = discord.Embed(colour=discord.Colour.green(),
                                  description=f"✅ Successfully deleted **{len(deleted)}** messages.")
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

    @app_commands.command(name="slowmode", description="Sets or removes slowmode in the current channel.")
    @is_staff_perms()
    @app_commands.default_permissions(manage_channels=True)
    async def slowmode_slash(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 0, 21600],
                             reason: str = None):
        await interaction.channel.edit(slowmode_delay=seconds, reason=reason)
        status = "disabled" if seconds == 0 else f"set to **{seconds} seconds**"
        embed = discord.Embed(colour=EMBED_COLOUR, title="__**Slowmode Updated**__",
                              description=f"✅ Slowmode has been {status}.\n**Reason:** {reason or 'No reason provided'}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lockdown", description="Prevents @everyone from sending messages.")
    @is_staff_perms()
    @app_commands.default_permissions(manage_channels=True)
    async def lockdown(self, interaction: discord.Interaction, reason: str = "No reason provided"):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        if overwrite.send_messages is False:
            return await interaction.response.send_message("⚠️ This channel is already locked.", ephemeral=True)

        overwrite.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(title="🛡️ Channel Locked", description=f"Reason: {reason}", colour=discord.Colour.red())
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unlock", description="Restores the ability for @everyone to speak.")
    @is_staff_perms()
    @app_commands.default_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        embed = discord.Embed(title="🔓 Channel Unlocked", description="Lockdown lifted.", colour=discord.Color.green())
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))