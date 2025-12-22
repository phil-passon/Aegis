import discord
import random
from discord.ext import commands
from discord import app_commands

from Main import NAME, BOT_INVITE, ICON_URL, EMBED_COLOUR, SOURCE_CODE, STAFF_ROLE_NAME

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rps", description="Play Rock, Paper, Scissors against the bot.")
    @app_commands.describe(choice="Your choice: rock, paper, or scissors.")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Rock", value="rock"),
        app_commands.Choice(name="Paper", value="paper"),
        app_commands.Choice(name="Scissors", value="scissors"),
    ])
    async def rps_slash(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        user_choice = choice.value
        comp_choice = random.choice(['rock', 'paper', 'scissors'])

        WIN_CONDITIONS = {('rock', 'scissors'), ('paper', 'rock'), ('scissors', 'paper')}

        if user_choice == comp_choice:
            result_title = 'Tie! 🤝'
            result_color = EMBED_COLOUR
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

    @app_commands.command(name="rr", description="Play Russian Roulette (chance of a loaded chamber).")
    async def rr_slash(self, interaction: discord.Interaction):
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

    @app_commands.command(name="flip", description="Flip a coin (Heads or Tails).")
    async def flip_slash(self, interaction: discord.Interaction):
        winner_message = random.choice(['Heads', 'Tails'])

        if winner_message == 'Heads':
            desc = "Heads 🪙"
            image_url = ICON_URL
        else:
            desc = "Tails 🪙"
            image_url = "https://iili.io/fCwxXON.png"

        embed = discord.Embed(colour=EMBED_COLOUR,
                              title="Coin Flip Winner:",
                              description=desc)
        embed.set_image(url=image_url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="poll", description="Creates a new poll. Separate options with commas.")
    @app_commands.describe(
        question="The question for the poll.",
        options_list="A comma-separated list of options (Min 2, Max 10)."
    )
    async def poll_slash(self, interaction: discord.Interaction, question: str, options_list: str):
        options = [opt.strip() for opt in options_list.split(',') if opt.strip()]
        emoji_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        if len(options) < 2 or len(options) > 10:
            return await interaction.response.send_message("A poll must have between 2 and 10 options.", ephemeral=True)

        poll_content = "\n".join(f"{emoji_list[i]} **{option}**" for i, option in enumerate(options))
        embed = discord.Embed(colour=EMBED_COLOUR, title=f"🗳️ | **{question}**", description=poll_content)
        embed.set_footer(text=f"Poll created by: {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.defer(thinking=True, ephemeral=True)
        poll_message = await interaction.channel.send(embed=embed)

        for i in range(len(options)):
            await poll_message.add_reaction(emoji_list[i])

        await interaction.followup.send("✅ Poll successfully created!", ephemeral=True)

    @app_commands.command(name="8ball", description="Ask the Magic 8-Ball a question.")
    @app_commands.describe(question="The question you want the 8-Ball to answer.")
    async def eightball_slash(self, interaction: discord.Interaction, question: str):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
            "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
            "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]

        answer = random.choice(responses)
        embed = discord.Embed(colour=EMBED_COLOUR, title="🎱 Magic 8-Ball",
                              description=f"**Question:** {question}\n\n**Answer:** {answer}")
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))