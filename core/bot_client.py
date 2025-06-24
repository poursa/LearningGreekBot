import discord
from discord.ext import commands
from config import GUILD_ID, EXTENSIONS
from core.sync_utils import should_sync, update_sync_timestamp

class LearningGreekBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.messages = True
        intents.members = True

        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        
        for ext in EXTENSIONS:
            await self.load_extension(ext)
        print("All extensions loaded.")

        if should_sync():
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print("Slash commands synced.")
            update_sync_timestamp()
        else:
            print("Skipping slash commands sync due to cooldown.")



