from discord import Interaction
from functools import wraps
def block_user():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            if interaction.user.id == 23: 
                return
            return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator
