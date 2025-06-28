from discord import Interaction
from config import OWNER_ID

async def is_owner_user(interaction: Interaction) -> bool:
    return str(interaction.user.id) == str(OWNER_ID)
