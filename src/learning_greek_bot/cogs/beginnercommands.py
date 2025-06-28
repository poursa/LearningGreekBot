from discord.ext import commands
from discord import app_commands
import discord
import asyncio
from ..config import CHANNEL_NAME
from ..core import decorators
from .base import BaseCog


class BeginnerCommands(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot, checks=[])

    @app_commands.command(
        name="welcomemembers",
        description="Gather users who got a rank and print a welcome message",
    )
    @decorators.log_action()
    async def welcomemembers(self, interaction: discord.Interaction):
        EXCLUDED_ROLES = {"Native", "Non-Learner"}

        await interaction.response.defer(thinking=True)

        guild = interaction.guild
        if not guild:
            await interaction.followup.send(
                "This command can only be used in a server."
            )
            return
        channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)

        if not channel:
            await interaction.followup.send("Channel not found.")
            return

        found_users = set()

        async for message in channel.history(limit=None, oldest_first=True):
            if "just got a rank!" in message.content.lower():
                for user in message.mentions:
                    try:
                        member = await guild.fetch_member(user.id)
                    except discord.NotFound:
                        continue

                    has_excluded = any(
                        role.name in EXCLUDED_ROLES for role in member.roles
                    )
                    if not has_excluded:
                        found_users.add(member.mention)

            await asyncio.sleep(0.2)

        if found_users:
            welcome_line = (
                " ".join(sorted(found_users))
                + "# Welcome everyone! What made you interested in modern Greek?"
            )
            print(welcome_line)
            await interaction.followup.send("Output printed to terminal.")
        else:
            print("No matching messages found.")
            await interaction.followup.send("No matching messages found.")
