import discord
from discord.ext import commands
from discord import app_commands
import random


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="slap", description="Slap another user with a random object!")
    @app_commands.describe(member="The person you want to slap.")
    async def slap(self, interaction: discord.Interaction, member: discord.Member):
        if member == interaction.user:
            return await interaction.response.send_message("You can't slap yourself! That's just sad.", ephemeral=True)

        objects = ["a wet fish", "a giant foam finger", "a keyboard", "the Sassy Intern's coffee mug",
                   "a stale baguette"]
        chosen_obj = random.choice(objects)

        await interaction.response.send_message(
            f"👋 {interaction.user.mention} slapped {member.mention} with **{chosen_obj}**!")

    @app_commands.command(name="rate", description="Let the bot rate something from 1-10.")
    @app_commands.describe(thing="The thing you want the bot to rate.")
    async def rate(self, interaction: discord.Interaction, thing: str):
        score = random.randint(1, 10)

        if score <= 3:
            comment = "Actual cringe. 0/10 would not recommend."
        elif score <= 7:
            comment = "It's fine, I guess. Perfectly average."
        else:
            comment = "Absolute perfection. This is peak performance."

        embed = discord.Embed(
            title="📊 Rating Results",
            description=f"**Thing:** {thing}\n**Score:** {score}/10\n\n*{comment}*",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="vibecheck", description="The bot determines your current vibe.")
    async def vibe_check(self, interaction: discord.Interaction):
        vibes = [
            "Manifesting Greatness ✨", "Main Character Energy 👑", "Pure Chaos 🌪️",
            "Low Battery 🔋", "Spicy 🌶️", "Cringe (Sorry) 😬", "Absolute Legend 🗿"
        ]

        vibe = random.choice(vibes)
        color = discord.Color.random()

        embed = discord.Embed(
            title=f"🔍 {interaction.user.display_name}'s Vibe Check",
            description=f"Current Status: **{vibe}**",
            color=color
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ship", description="Check the compatibility between two users.")
    @app_commands.describe(user1="First person", user2="Second person")
    async def ship(self, interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
        percent = random.randint(0, 100)

        if percent < 30:
            msg = "Yikes. Best to stay as distant acquaintances. 🛑"
        elif percent < 70:
            msg = "There's a spark! Maybe try a coffee date? ☕"
        else:
            msg = "A match made in heaven! Get the wedding cake ready. 🎂"

        embed = discord.Embed(
            title="❤️ Compatibility Meter",
            description=f"**{user1.display_name}** & **{user2.display_name}**\nResult: **{percent}%**\n\n*{msg}*",
            color=discord.Color.magenta()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Social(bot))