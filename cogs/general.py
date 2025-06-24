from discord.ext import commands
from discord import app_commands
import discord

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("General cog ready.")

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction: discord.Interaction):
        websocket_latency = round(self.bot.latency * 1000)
        before = discord.utils.utcnow()
        await interaction.response.send_message("Pinging...")
        after = discord.utils.utcnow()
        message_latency = round((after - before).total_seconds() * 1000)
        await interaction.edit_original_response(content=f"Pong! \nWebsocket latency: {websocket_latency}ms\nMessage latency: {message_latency}ms")


async def setup(bot):
    await bot.add_cog(General(bot))
