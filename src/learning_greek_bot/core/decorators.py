from functools import wraps

from discord import Interaction, Member, app_commands


def log_action():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            if not isinstance(interaction.command, app_commands.Command):
                raise TypeError("Expected interaction to be of type discord.Interaction")
            time = interaction.created_at.strftime("%Y-%m-%d %H:%M:%S")
            guild_name = interaction.guild.name if interaction.guild else "DMs"
            guild_id = interaction.guild.id if interaction.guild else "DMs"
            print(
                f"[{time}] {interaction.user.name} ({interaction.user.id}) called command "
                + f"{interaction.command.name} in guild {guild_name} (ID: {guild_id})"
            )
            return await func(self, interaction, *args, **kwargs)

        return wrapper

    return decorator


def admin_only():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            if (
                not interaction.user
                or not isinstance(interaction.user, Member)
                or not interaction.user.guild_permissions.administrator
            ):
                await interaction.response.send_message("You do not have permission to use this command.")
                return
            return await func(self, interaction, *args, **kwargs)

        return wrapper

    return decorator
