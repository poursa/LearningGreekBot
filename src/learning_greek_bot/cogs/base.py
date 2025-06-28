from discord import app_commands
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot, checks: list | None = None):
        self.bot = bot
        self._checks = checks or []
        self.add_checks()

    def getcommand(self, attr: str) -> app_commands.Command | None:
        maybe_cmd = getattr(self, attr, None)
        if isinstance(maybe_cmd, app_commands.Command):
            return maybe_cmd
        return None

    def add_checks(self) -> list[app_commands.Command]:
        commands = []
        for attr in dir(self):
            cmnd = self.getcommand(attr)
            for check in self._checks:
                if cmnd:
                    cmnd.add_check(check)
        return commands
