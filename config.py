import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
CHANNEL_NAME = os.getenv("DISCORD_CHANNEL_NAME", "new-members")
SYNC_DELAY_MINUTES = int(os.getenv("SYNC_DELAY_MINUTES", 0))
SYNC_TIMESTAMP_FILE = "data/last_sync.txt"
EXTENSIONS = [
    "cogs.general",
    "cogs.welcome"
]

