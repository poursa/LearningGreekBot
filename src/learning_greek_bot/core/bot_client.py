import importlib
import inspect

import discord
from discord.ext import commands

from ..cogs.base import BaseCog
from ..config import EXTENSIONS
from .utils import should_sync, update_sync_timestamp


class LearningGreekBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.messages = True
        intents.members = True

        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        for ext in EXTENSIONS:
            try:
                mod = importlib.import_module(ext)
            except ModuleNotFoundError as e:
                print(f"Failed to load extension {ext}: {e}")
                continue
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and issubclass(obj, BaseCog) and obj is not BaseCog:
                    await self.add_cog(obj(self))
                    print(f"Loaded: {name}")
        print("All extensions loaded.")

        if should_sync():
            synced = await self.tree.sync()
            print(f"{synced.__len__()} slash commands synced.")
            update_sync_timestamp()
        else:
            print("Skipping slash commands sync due to cooldown.")
