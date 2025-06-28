import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
CHANNEL_NAME = os.getenv("DISCORD_CHANNEL_NAME", "new-members")
SYNC_DELAY_MINUTES = int(os.getenv("SYNC_DELAY_MINUTES", 1))
SYNC_TIMESTAMP_FILE = Path("data/last_sync.txt")
OWNER_ID = os.getenv("DISCORD_OWNER_ID")
EXTENSIONS = [
    "learning_greek_bot.cogs.general",
    "learning_greek_bot.cogs.faq",
    "learning_greek_bot.cogs.beginnercommands",
    "learning_greek_bot.cogs.admindev",
    "learning_greek_bot.cogs.markov",
]
