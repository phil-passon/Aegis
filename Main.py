# -----------------------------------Setup--------------------------------------#
import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------Configuration--------------------------------------#
NAME = 'Aegis'
BOT_INVITE = "https://discord.com/oauth2/authorize?client_id=1443892177951526972&permissions=8&integration_type=0&scope=applications.commands+bot"
ICON_URL = "https://iili.io/fChSV49.png"
EMBED_COLOUR = discord.Color.from_rgb(219, 196, 164)
STAFF_ROLE_NAME = 'StaffPerms'
SOURCE_CODE = "https://github.com/phil-passon/Aegis"


# -----------------------------------Client Setup--------------------------------------#

class AegisBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=[],
            help_command=None,
            intents=intents
        )

    async def setup_hook(self):
        print("--- Loading Cogs ---")
        # This will load Moderation.py, Info.py, and Fun.py
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    # filename[:-3] removes the .py
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"✅ Loaded: {filename}")
                except Exception as e:
                    print(f"❌ Failed to load {filename}: {e}")

        print("\nSyncing Slash Commands...")
        await self.tree.sync()


# -----------------------------------Events--------------------------------------#

bot = AegisBot()


@bot.event
async def on_ready():
    print(f"🤖 {bot.user.name} is online and ready.")
    bot.loop.create_task(status_task())


async def status_task():
    statuses = [discord.Game("Use /help for commands"), discord.Game("Version 1.1.0")]
    while True:
        for status in statuses:
            await bot.change_presence(activity=status)
            await asyncio.sleep(5)


if __name__ == "__main__":
    bot.run(os.environ.get("DISCORD_BOT_TOKEN"))