from discord.ext import commands
from discord import Interaction, app_commands
from core.utils import getcommand


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot, checks=None):
        self.bot = bot
        self._checks = checks or []
        self.add_checks()
    
    def add_checks(self) -> list[app_commands.Command]:
        commands = []
        for attr in dir(self):
            cmnd = getcommand(self, attr)
            for check in self._checks:
                if cmnd:
                    cmnd.add_check(check)
        return commands
