import discord
from discord.ext import commands
from discord import app_commands

from Main import NAME, BOT_INVITE, ICON_URL, EMBED_COLOUR, SOURCE_CODE, STAFF_ROLE_NAME


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def is_staff():
        async def predicate(interaction: discord.Interaction) -> bool:
            if discord.utils.get(interaction.user.roles, name=STAFF_ROLE_NAME):
                return True
            err = discord.Embed(colour=discord.Color.red(), title="Error", description="Missing StaffPerms.")
            await interaction.response.send_message(embed=err, ephemeral=True)
            return False
        return app_commands.check(predicate)

    @app_commands.command(name="help", description="Shows a list of all bot commands.")
    async def help_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=EMBED_COLOUR,
                              title="Aegis Bot Commands",
                              description="A List of all the commands")
        embed.add_field(name="📑| **Info**",
                        value="``/help`` | ``/team`` | ``/about`` |  ``/whois`` |  ``/avatar`` | ``/serverinfo``",
                        inline=False)

        embed.add_field(name="💸| **Moderation** (Requires StaffPerms)",
                        value="``/embed`` | ``/kick`` | ``/ban`` | ``/unban`` | ``/clear`` | ``/slowmode`` | ``/lockdown`` | ``/unlock`` | ``/nuke``",
                        inline=False)

        embed.add_field(name="👨‍💻| **Support**",
                        value="``/ticket`` | ``/close``",
                        inline=False)

        embed.add_field(name="⚡️| **Fun**",
                        value="``/rps`` | ``/rr`` | ``/flip`` | ``/poll`` | ``/8ball``",
                        inline=False)

        embed.add_field(name="🔗| ** Links**",
                        value=f"❤️| [**Invite**]({BOT_INVITE}) | 👨‍💻️| [**Source Code**]({SOURCE_CODE})",
                        inline=False)
        embed.set_author(name=NAME, url=BOT_INVITE, icon_url=ICON_URL)
        embed.set_footer(text=f"Requested by {interaction.user.name}",
                         icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Shows detailed information about the server.")
    async def serverinfo_slash(self, self_interaction: discord.Interaction):
        guild = self_interaction.guild

        time_since_creation = discord.utils.format_dt(guild.created_at, "R")
        member_count = len([m for m in guild.members if not m.bot])
        bot_count = len([m for m in guild.members if m.bot])
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count

        embed = discord.Embed(
            title=f"🏛️ | Server Info: {guild.name}",
            colour=EMBED_COLOUR
        )

        embed.add_field(name="Owner", value=guild.owner.mention, inline=False)
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=False)
        embed.add_field(name="Created", value=f"<t:{int(guild.created_at.timestamp())}:F> ({time_since_creation})",
                        inline=False)
        embed.add_field(name="Members", value=f"👥 {member_count} humans\n🤖 {bot_count} bots", inline=False)
        embed.add_field(name="Channels", value=f"💬 {text_channels} text\n🔊 {voice_channels} voice", inline=False)
        embed.add_field(name="Roles", value=f"🎗️ {len(guild.roles)} roles", inline=False)
        embed.add_field(name="Boost Level", value=f"Tier {boost_level} ({boost_count} boosts)", inline=False)
        embed.add_field(name="Verification Level", value=str(guild.verification_level).capitalize().replace('_', ' '),
                        inline=False)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            embed.set_author(name=guild.name, icon_url=guild.icon.url)

        embed.set_footer(text=f"Requested by {self_interaction.user.name}",
                         icon_url=self_interaction.user.display_avatar.url)

        await self_interaction.response.send_message(embed=embed)

    @app_commands.command(name="about", description="Shows information about the bot.")
    async def about_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=EMBED_COLOUR,
                              title="🤖| **Botinfo**",
                              description="Aegis is a Bot that helps you run a professional discord Server. "
                                          "\r\nThe development was started on 28th of November of 2025."
                                          "\r\nTo get the list of team members use ``/team`` ")

        embed.add_field(name="🐍| **Library**", value="discord.py")
        embed.add_field(name="💎| **Invite**", value=f"[Click here]({BOT_INVITE})")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="whois", description="Shows detailed information about a user.")
    @app_commands.describe(user="The member to get information about (defaults to yourself).")
    async def whois_slash(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        title = f"Your info" if target == interaction.user else f"{target.name}'s info"
        roles = [role.mention for role in target.roles if role.name != "@everyone"]
        roles.reverse()

        embed = discord.Embed(title=title, colour=EMBED_COLOUR)
        embed.set_author(name=target, icon_url=target.display_avatar.url)
        embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="👀 | **Username**", value=target.name, inline=False)
        embed.add_field(name="🔖 | **ID**", value=target.id, inline=False)
        embed.add_field(name="⬆️ | **Highest Role**", value=target.top_role.mention)
        embed.add_field(name=f"📟 | **Roles ({len(target.roles) - 1})**",
                        value=" ".join(roles) if roles else "No other roles.",
                        inline=False)
        embed.add_field(name="💡 | **Joined**",
                        value=f"<t:{int(target.joined_at.timestamp())}:F>", inline=True)
        embed.add_field(name="📲 | **Created**",
                        value=f"<t:{int(target.created_at.timestamp())}:F>", inline=True)

        embed.set_footer(text=f"Requested by {interaction.user.name}",
                         icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Shows the user's avatar.")
    async def avatar_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=EMBED_COLOUR, title="Bot Avatar")
        embed.set_image(url=self.bot.user.display_avatar.url)  # Access bot via self.bot

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="team", description="Lists the members of the bot development team.")
    async def team_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(colour=EMBED_COLOUR, title="Team Members:")
        embed.add_field(name="👑 |**Owner and Main Programmer:**",
                        value="<@604615168047185926>")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))