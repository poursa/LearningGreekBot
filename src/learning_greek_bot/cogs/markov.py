# features/markov.py
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

import discord
import markovify
from discord import app_commands
from tqdm.asyncio import tqdm

from ..core import decorators
from ..core.utils import sanitize_sentence
from .base import BaseCog


def encode_message(raw_msg: str) -> str:
    """
    Encodes a message for Markov processing by sanitizing and escaping special characters.
    """
    return sanitize_sentence(raw_msg).replace("\\", "\\\\").replace("\n", " \\n ")


def decode_message(encoded_msg: str) -> str:
    """
    Decodes a message encoded for Markov processing by replacing escaped characters with their original form.
    """
    return sanitize_sentence(encoded_msg).replace("\\n", "\n").replace("\\\\", "\\")


class Markov(BaseCog):
    model: markovify.NewlineText | None
    source_file: Path
    generating: bool
    state_size: int
    current_user: discord.User | None

    def __init__(self, bot):
        super().__init__(bot, checks=[])
        self.model = None
        self.source_file = Path("data/markov_input.txt")
        self.generating = False
        self.state_size = 2
        self.current_user = None

    def train(self, text: list[str]):
        """
        Train the Markov model with the provided text.
        """
        if not text:
            raise ValueError("No text provided for training.")
        self.model = markovify.NewlineText("\n".join(text), state_size=self.state_size)

    @app_commands.command(
        name="gather_markov_data",
        description="Train a Markov model from your messages in this channel.",
    )
    @app_commands.describe(days_lookback="Number of days to look back for messages to train on (default is 1 day).")
    @app_commands.default_permissions(administrator=True)
    @decorators.log_action()
    @decorators.admin_only()
    async def gather_markov_data(self, interaction: discord.Interaction, days_lookback: int = 1):
        if self.generating:
            await interaction.response.send_message(
                "A training session is already in progress. Please wait until it finishes."
            )
            return
        self.generating = True
        try:
            await interaction.response.send_message("Starting data collection, this might take a while...")
            channel = interaction.channel
            if channel is None:
                print("[ERROR] No channel found for data collection.")
                return
            if isinstance(channel, discord.ForumChannel | discord.CategoryChannel):
                print("[ERROR] Invoked in a Forum or Category channel.")
                return
            cutoff = datetime.now(UTC) - timedelta(days=days_lookback)
            collected = []

            messages = []
            with tqdm(
                desc="Collecting messages",
                unit="hours of messages",
                total=days_lookback * 24,
            ) as pbar:
                last_hour = -1
                async for msg in channel.history(limit=None, after=cutoff):
                    messages.append(msg)
                    hours_done = int((msg.created_at - cutoff).total_seconds() // 3600)
                    if hours_done != last_hour:
                        pbar.update(hours_done - last_hour)
                        last_hour = hours_done

            await channel.send(f"Total messages: {len(messages)}")
            for msg in messages:
                content = encode_message(msg.content)
                if content.strip() == "":
                    continue
                content = f"{msg.author.id}: {content}"
                collected.append(content)

            if not collected:
                await channel.send("No messages found to train on.")
                return

            self.source_file.parent.mkdir(parents=True, exist_ok=True)
            self.source_file.write_text("\n".join(collected), encoding="utf-8")

            print(f"Collected {len(collected)} messages. Model is ready for training.")
            await channel.send(f"Collected {len(collected)} messages. Model is ready for training.")
        finally:
            self.generating = False

    @app_commands.command(
        name="train_markov_model",
        description="Generate a sentence using the trained Markov model.",
    )
    @app_commands.describe(
        user="User to train the model on (default is all users).",
        greek_only="Whether to only include Greek messages (default is True).",
    )
    @decorators.log_action()
    async def train_markov_model(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None,
        greek_only: bool = True,
    ):
        await interaction.response.defer(thinking=True)
        if not self.source_file.exists():
            await interaction.followup.send("No source file found. Please run /gather_markov_data first.")
            return
        with self.source_file.open(encoding="utf-8") as f:
            messages = []
            for line in f.readlines():
                match = re.match(r"^(?P<user_id>\d+):\s*(?P<content>.*)$", line)
                if not match:
                    continue
                msg_user = match.group("user_id")
                msg_content = match.group("content")
                if user and str(user.id) != msg_user:
                    continue
                if greek_only and re.search(r"[a-mo-zA-Z]|^n|[^\\]n", msg_content):
                    continue
                messages.append(msg_content)
        if not messages:
            await interaction.followup.send("No valid messages found to train the model.")
            return
        if user:
            self.current_user = user
        self.model = markovify.NewlineText("\n".join(messages), state_size=self.state_size)

        await interaction.followup.send(
            f"Markov model trained successfully on {len(messages)} messages." if self.model else "No model found."
        )

    @app_commands.command(
        name="generate_message",
        description="Generate a sentence using the trained Markov model.",
    )
    @decorators.log_action()
    async def generate_message(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        if not self.model:
            await interaction.followup.send(f"No model found. Run /{self.train_markov_model.name} first.")
            return
        if not interaction.guild:
            await interaction.followup.send("This command can only be used in a server.")
            return
        sentence = self.model.make_short_sentence(200, tries=100)
        if sentence is None:
            await interaction.followup.send("Failed to generate a sentence.")
        else:
            sentence = decode_message(sentence)
            if self.current_user is None:
                user_prefix = ""
            else:
                user_prefix = f"{self.current_user.display_name}: "
            await interaction.followup.send(f"{user_prefix}{sentence}")
