# features/markov.py

import discord
from discord import app_commands
import asyncio
from datetime import datetime, timedelta, timezone
import markovify
import os
import re
from cogs.base import BaseCog


class Markov(BaseCog):
    def __init__(self, bot):
        super().__init__(bot, checks=[])
        self.model = None
        self.source_file = "data/markov_input.txt"
        self.generating = False

    @app_commands.command(name="train_markov", description="Train a Markov model from your messages in this channel.")
    async def train_markov(self, interaction: discord.Interaction):
        if self.generating:
            await interaction.response.send_message("❌ A training session is already in progress. Please wait until it finishes.")
            return
        self.generating = True
        try:
            await interaction.response.defer(thinking=True)
            sleep_time = 0.02
            channel = interaction.channel
            author_id = interaction.user.id
            cutoff = datetime.now(timezone.utc) - timedelta(days=60)
            start_time = datetime.now(timezone.utc)
            collected = []

            def is_non_latin(text):
                return not re.search(r'[a-zA-Z]', text)


            for i in range(2):
                try:
                    async for msg in channel.history(limit=None, after=cutoff, oldest_first=True):
                        if (msg.author.id == author_id or msg.author.id == 311238703295102976 or msg.author.id == 434288236752273419) and is_non_latin(msg.content):
                            collected.append(msg.content.strip())
                            #print(f"Collected message date {msg.created_at}")
                        await asyncio.sleep(sleep_time)
                    break
                except discord.Forbidden:
                    collected = []
                    print("Slowing down due to rate limits, retrying...")
                    sleep_time = 0.05

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
            await interaction.channel.send(f"Trained on {len(collected)} messages in {durataion_mins if duration > 60 else duration} seconds. Model is ready for use.")
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
