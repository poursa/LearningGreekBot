from discord.ext import commands
from discord import  Permissions, app_commands
import discord
from cogs.base import BaseCog
from core.check_utils import is_owner_user
from core.utils import getcommand
from core import decorators


class AdminDev(BaseCog):
    def __init__(self, bot: commands.Bot):
        checks = [
            is_owner_user
        ]
        super().__init__(bot, checks=checks)
        for attr in dir(self):
            cmnd = getcommand(self, attr)
            if cmnd:
                cmnd.default_permissions = Permissions(administrator=True)


    @app_commands.command(name="admindev", description="tyes command test")
    @decorators.log_action()
    async def admindev(self, interaction: discord.Interaction):
        await interaction.response.send_message("admin dev test")
