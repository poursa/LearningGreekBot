import discord
from discord import Permissions, app_commands
from discord.ext import commands

from ..core import decorators
from ..core.check_utils import is_owner_user
from .base import BaseCog


class AdminDev(BaseCog):
    def __init__(self, bot: commands.Bot):
        checks = [is_owner_user]
        super().__init__(bot, checks=checks)
        for attr in dir(self):
            cmnd = self.getcommand(attr)
            if cmnd:
                cmnd.default_permissions = Permissions(administrator=True)

    @app_commands.command(name="admindev", description="tyes command test")
    @decorators.log_action()
    async def admindev(self, interaction: discord.Interaction):
        await interaction.response.send_message("admin dev test")
