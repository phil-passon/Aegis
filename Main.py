# -----------------------------------Setup--------------------------------------#
import os
from dotenv import load_dotenv # NEW: Import load_dotenv

load_dotenv() # NEW: Load variables from the .env file immediately
import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import random

# -----------------------------------Intents--------------------------------------#
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# -----------------------------------Configuration--------------------------------------#

name = 'Aegis'
bot_invite = "https://discord.com/oauth2/authorize?client_id=1443892177951526972&permissions=8&integration_type=0&scope=applications.commands+bot"
icon_url = "https://iili.io/fChSV49.png"
embed_color = discord.Color.from_rgb(219, 196, 164)
STAFF_ROLE_NAME = 'StaffPerms'

# -----------------------------------Client Setup--------------------------------------#

client = commands.Bot(command_prefix=None,
                      help_command=None,
                      case_insensitive=True,
                      intents=intents)


# -----------------------------------Hooks and Sync--------------------------------------#

@client.event
async def on_ready():
    print(f"🤖 Bot ({client.user.name}) is online.")
    print(f"ID: {client.user.id}")
    client.loop.create_task(status_task())


@client.event
async def setup_hook():
    print("Initiating GLOBAL slash command sync...")
    await client.tree.sync()
    print("Global slash command sync requested.")


async def status_task():
    statuses = [
        discord.Game("Use /help for help"),
        discord.Game("Version 1.0.0")
    ]
    while True:
        for status in statuses:
            await client.change_presence(activity=status, status=discord.Status.online)
            await asyncio.sleep(5)


# -----------------------------------Wichtig--------------------------------------#

@client.event
async def on_guild_join(guild):
    staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)
    if not staff_role:
        staff_role = await guild.create_role(name=STAFF_ROLE_NAME)

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                colour=embed_color,
                title="__**Aegis**__",
                description="Hi! I'm Aegis, here to help you run an amazing server. "
                            f"\r\n\r\n**Action Required:** Please assign the role ``{STAFF_ROLE_NAME}`` "
                            "to all staff members to grant them access to moderation commands."
            )
            embed.add_field(name="🔗| ** Links**",
                            value=f"[❤️|**Invite**]({bot_invite})",
                            inline=False)
            await channel.send(embed=embed)
            break


# -----------------------------------Slash Command Checks--------------------------------------#

def is_staff_perms():
    async def predicate(interaction: discord.Interaction) -> bool:
        if discord.utils.get(interaction.user.roles, name=STAFF_ROLE_NAME):
            return True
        else:
            error_embed = discord.Embed(
                colour=discord.Colour.red(),
                title="__**Error**__",
                description="You don't have the required ``StaffPerms`` role to use this command."
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return False

    return app_commands.check(predicate)


# -----------------------------------Slash Commands--------------------------------------#

# --- Info Commands ---

@client.tree.command(name="help", description="Shows a list of all bot commands.")
async def help_slash(interaction: discord.Interaction):
    embed = discord.Embed(colour=embed_color,
                          title="Aegis Bot Commands",
                          description="Use `/` to see all commands!")
    embed.add_field(name="📑| **Info**",
                    value="``/help`` | ``/team`` | ``/about`` |  ``/whois`` |  ``/avatar``",
                    inline=False)

    embed.add_field(name="💸| **Moderation** (Requires StaffPerms)",
                    value="``/embed`` | ``/kick`` | ``/ban`` | ``/unban``",
                    inline=False)

    embed.add_field(name="⚡️| **Fun**",
                    value="``/rps`` | ``/rr`` | ``/flip``",
                    inline=False)

    embed.add_field(name="🔗| ** Links**",
                    value=f"[❤️|**Invite**]({bot_invite})",
                    inline=False)
    embed.set_author(name=name, url=bot_invite, icon_url=icon_url)
    embed.set_footer(text=f"Information requested by: {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="about", description="Shows information about the bot.")
async def about_slash(interaction: discord.Interaction):
    embed = discord.Embed(colour=embed_color,
                          title="🤖| **Botinfo**",
                          description="Aegis is a Bot that helps you run a professional discord Server. "
                                      "\r\nThe development was started on 28th of November of 2025."
                                      "\r\nTo get the list of team members use ``/team`` ")

    embed.add_field(name="🐍| **Library**", value="discord.py")
    embed.add_field(name="💎| **Invite**", value=f"[Click here]({bot_invite})")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="whois", description="Shows detailed information about a user.")
@app_commands.describe(user="The member to get information about (defaults to yourself).")
async def whois_slash(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    title = f"Your info" if target == interaction.user else f"{target.name}'s info"
    roles = [role.mention for role in target.roles if role.name != "@everyone"]
    roles.reverse()

    embed = discord.Embed(title=title, colour=embed_color)
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


@client.tree.command(name="avatar", description="Shows the bot's avatar.")
async def avatar_slash(interaction: discord.Interaction):
    embed = discord.Embed(colour=embed_color, title="Bot Avatar")
    embed.set_image(url=client.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="team", description="Lists the members of the bot development team.")
async def team_slash(interaction: discord.Interaction):
    embed = discord.Embed(colour=embed_color, title="Team Members:")
    embed.add_field(name="👑 |**Owner and Main Programmer:**",
                    value="<@604615168047185926>")

    await interaction.response.send_message(embed=embed)


# --- Moderation Commands ---

@client.tree.command(name="embed", description="Generates a simple embed from your text.")
@is_staff_perms()
@app_commands.describe(message="The text content for the embed description.")
async def embed_slash(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(
        "Sending embed...",
        ephemeral=True,
        delete_after=3
    )

    embed = discord.Embed(colour=discord.Colour.blue(),
                          title="",
                          description=message)

    embed.add_field(name="\u200b", value=f"[Invite]({bot_invite})")

    await interaction.channel.send(embed=embed)


@client.tree.command(name="kick", description="Kicks a member from the server.")
@is_staff_perms()
@app_commands.default_permissions(kick_members=True)
@app_commands.describe(member="The member to kick.", reason="The reason for the kick.")
async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if member.top_role >= interaction.user.top_role:
        desc = "You cannot kick a member with an equal or higher role than you."
    elif member.top_role >= interaction.guild.me.top_role:
        desc = f"I cannot kick {member.display_name} as their highest role is equal to or higher than my own."
    else:
        await member.kick(reason=reason)
        embed = discord.Embed(colour=embed_color,
                              title=f'__**Kicked**__',
                              description=f'**Member**:{member.mention}\r\n**Reason**: {reason or "No reason provided"} ')
        await interaction.response.send_message(embed=embed)
        return

    error_embed = discord.Embed(colour=discord.Colour.red(), title="__**Error**__", description=desc)
    await interaction.response.send_message(embed=error_embed, ephemeral=True)


@client.tree.command(name="ban", description="Bans a member from the server.")
@is_staff_perms()
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(member="The member to ban.", reason="The reason for the ban.")
async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if member.top_role >= interaction.user.top_role:
        desc = "You cannot ban a member with an equal or higher role than you."
    elif member.top_role >= interaction.guild.me.top_role:
        desc = f"I cannot ban {member.display_name} as their highest role is equal to or higher than my own."
    else:
        await member.ban(reason=reason)
        embed = discord.Embed(colour=embed_color,
                              title=f'__**Banned**__',
                              description=f'**Member:**{member.mention}\r\n**Reason:** {reason or "No reason provided"} ')
        await interaction.response.send_message(embed=embed)
        return

    error_embed = discord.Embed(colour=discord.Colour.red(), title="__**Error**__", description=desc)
    await interaction.response.send_message(embed=error_embed, ephemeral=True)


@client.tree.command(name="unban", description="Unbans a user using their ID.")
@is_staff_perms()
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(user_id="The ID of the user to unban.", reason="The reason for the unban.")
async def unban_slash(interaction: discord.Interaction, user_id: str, reason: str = None):
    try:
        target_id = int(user_id)

        user_name = f"User ID: `{target_id}`"
        banned_users = [entry async for entry in interaction.guild.bans()]
        unban_entry = discord.utils.find(lambda entry: entry.user.id == target_id, banned_users)

        if not unban_entry:
            error_embed = discord.Embed(
                colour=discord.Colour.orange(),
                title="__**Unban Error**__",
                description=f"User with ID **{user_id}** is not currently banned."
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        user_name = f"<@{target_id}> ({unban_entry.user.name})"

        await interaction.guild.unban(unban_entry.user, reason=reason)

        embed = discord.Embed(
            colour=discord.Colour.green(),
            title=f'__**Unbanned**__',
            description=f'**User:** {user_name}\r\n**Reason:** {reason or "No reason provided"}'
        )
        await interaction.response.send_message(embed=embed)

    except ValueError:
        error_embed = discord.Embed(
            colour=discord.Colour.red(),
            title="__**Error**__",
            description="Invalid User ID format. The ID must be a numeric value."
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

    except discord.Forbidden:
        error_embed = discord.Embed(
            colour=discord.Colour.red(),
            title="__**Permissions Error**__",
            description="I do not have the necessary permissions (Ban Members) to unban users."
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)

    except Exception as e:
        print(f"Unban error: {e}")
        error_embed = discord.Embed(
            colour=discord.Colour.red(),
            title="__**Unexpected Error**__",
            description="An unexpected error occurred during the unban process."
        )
        await interaction.response.send_message(embed=error_embed, ephemeral=True)


# --- Fun Commands ---

@client.tree.command(name="rps", description="Play Rock, Paper, Scissors against the bot.")
@app_commands.describe(choice="Your choice: rock, paper, or scissors.")
@app_commands.choices(choice=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
])
async def rps_slash(interaction: discord.Interaction, choice: app_commands.Choice[str]):
    user_choice = choice.value
    comp_choice = random.choice(['rock', 'paper', 'scissors'])

    WIN_CONDITIONS = {('rock', 'scissors'), ('paper', 'rock'), ('scissors', 'paper')}

    if user_choice == comp_choice:
        result_title = 'Tie! 🤝'
        result_color = embed_color
    elif (user_choice, comp_choice) in WIN_CONDITIONS:
        result_title = 'You win! 🎉'
        result_color = discord.Color.green()
    else:
        result_title = 'I win! 🤖'
        result_color = discord.Color.red()

    embed = discord.Embed(colour=result_color,
                          title=result_title,
                          description=f"Your choice: **{user_choice.capitalize()}**\nMy choice: **{comp_choice.capitalize()}**")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="rr", description="Play Russian Roulette (chance of a loaded chamber).")
async def rr_slash(interaction: discord.Interaction):
    is_dead = random.randint(0, 5) == 0

    if is_dead:
        embed = discord.Embed(colour=discord.Colour.red(),
                              title="Russian Roulette:",
                              description="*Click*. Loaded! You're dead 💀")
    else:
        embed = discord.Embed(colour=discord.Color.green(),
                              title="Russian Roulette:",
                              description="*Click*. Empty! You're good ✅")

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="flip", description="Flip a coin (Heads or Tails).")
async def flip_slash(interaction: discord.Interaction):
    winner_message = random.choice(['Heads', 'Tails'])

    if winner_message == 'Heads':
        desc = "Heads 🪙"
        image_url = icon_url

    else:
        desc = "Tails 🪙"
        image_url = "https://iili.io/fCwxXON.png"

    embed = discord.Embed(colour=embed_color,
                          title="Coin Flip Winner:",
                          description=desc)
    embed.set_image(url=image_url)

    await interaction.response.send_message(embed=embed)


# -----------------------------------Run Bot--------------------------------------#
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not BOT_TOKEN:
    print("FATAL ERROR: DISCORD_BOT_TOKEN environment variable is not set. Cannot run bot.")
else:
    client.run(BOT_TOKEN)