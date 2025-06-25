# features/markov.py

import discord
from discord import app_commands
import asyncio
from datetime import datetime, timedelta, timezone
import markovify
import os
import re
from cogs.base import BaseCog
from discord.message import Message

class Markov(BaseCog):
    def __init__(self, bot):
        super().__init__(bot, checks=[])
        self.model = None
        self.source_file = "data/markov_input.txt"
        self.generating = False

    @app_commands.command(name="train_markov", description="Train a Markov model from your messages in this channel.")
    @app_commands.describe(days_lookback="Number of days to look back for messages to train on (default is 1 day).")
    async def train_markov(self, interaction: discord.Interaction, days_lookback: int = 1):
        if self.generating:
            await interaction.response.send_message("❌ A training session is already in progress. Please wait until it finishes.")
            return
        self.generating = True
        try:
            await interaction.response.send_message('✅ Starting training, this might take a while...')

            processed = 0
            channel = interaction.channel
            author_id = interaction.user.id
            cutoff = datetime.now(timezone.utc) - timedelta(days=days_lookback)
            start_time = datetime.now(timezone.utc)
            collected = []
            messages:list[Message] = [msg async for msg in channel.history(limit=None, after=cutoff)]
            total_messages = len(messages)


            def is_non_latin(text):
                return not re.search(r'[a-zA-Z]', text) and text.strip()

            await interaction.response.send(f"Starting data collection... Total messages: {total_messages}")
            for msg in messages:
                if (msg.author.id == author_id or msg.author.id == 311238703295102976 or msg.author.id == 434288236752273419) and is_non_latin(msg.content):
                    collected.append(msg.content.strip())
                processed += 1
                if processed % max(total_messages // 10, 1) == 0:
                    percent = (processed / total_messages) * 100
                    print(f"Training progress: {percent:.1f}% ({processed}/{total_messages})")


            if not collected:
                await interaction.followup.send("No messages found to train on.")
                return

            os.makedirs("data", exist_ok=True)
            with open(self.source_file, "w", encoding="utf-8") as f:
                f.write("\n".join(collected))

            self.model = markovify.NewlineText("\n".join(collected), state_size=2)
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            durataion_mins = duration / 60
            print(f"Trained on {len(collected)} messages in {durataion_mins if duration > 60 else duration:.2f} seconds. Model is ready for use.")
            await interaction.channel.send(f"Trained on {len(collected)} messages in {durataion_mins if duration > 60 else duration:.2f} seconds. Model is ready for use.")
        finally:
            self.generating = False

    @app_commands.command(name="generate_message", description="Generate a sentence using the trained Markov model.")
    async def generate_message(self, interaction: discord.Interaction):
        if not self.model and os.path.exists(self.source_file):
            with open(self.source_file, encoding="utf-8") as f:
                text = f.read()
            self.model = markovify.NewlineText(text, state_size=2)

        if not self.model:
            await interaction.response.send_message("❌ No model found. Run /train_markov first.")
            return

        sentence = self.model.make_short_sentence(400, 20, tries = 40)
        await interaction.response.send_message(sentence or "🤖 Failed to generate a sentence.")
