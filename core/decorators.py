from discord import Interaction
from functools import wraps

def log_action():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            time = interaction.created_at.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{time}] {interaction.user.name} ({interaction.user.id}) called command '{interaction.command.name}' in guild '{interaction.guild.name}' (ID: {interaction.guild.id})")            
            return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator

def admin_only():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("You do not have permission to use this command.")
                return
            return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator
