from discord.ext import commands
from discord import app_commands
import discord
from data.faq_answers  import faq_answers

class FrequentlyAskedQuestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="faq", description="Get answers to frequently asked questions")
    @app_commands.describe(topic="The FAQ you want to learn about")
    async def faq(self, interaction: discord.Interaction, topic: str):
        
        
        response_text = faq_answers.get(topic.lower().strip(), "Sorry, I don't have information about that topic. Available topics: " + "\n    ".join(faq_answers.keys()))
        await interaction.response.send_message(response_text)


async def setup(bot):
    await bot.add_cog(FrequentlyAskedQuestions(bot))
