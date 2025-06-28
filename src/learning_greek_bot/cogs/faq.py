import discord
from discord.ext import commands
from discord import app_commands

from .base import BaseCog
from ..core import decorators
from ..data.faq_answers import faq_answers


class FrequentlyAskedQuestions(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot, checks=[])

    @app_commands.command(
        name="faq", description="Get answers to frequently asked questions"
    )
    @app_commands.describe(topic="The FAQ you want to learn about")
    @decorators.log_action()
    async def faq(self, interaction: discord.Interaction, topic: str):
        response_text = faq_answers.get(
            topic.lower().strip(),
            "Sorry, I don't have information about that topic.\n Available topics: \n"
            + "\n    ".join(faq_answers.keys()),
        )
        await interaction.response.send_message(response_text)
