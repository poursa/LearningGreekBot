from core.bot_client import LearningGreekBot
from config import TOKEN

bot = LearningGreekBot()

if __name__ == "__main__":
    bot.run(TOKEN)
