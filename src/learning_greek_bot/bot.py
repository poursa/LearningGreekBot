from core.bot_client import LearningGreekBot
from config import TOKEN

def main() -> None:
    bot = LearningGreekBot()
    bot.run(TOKEN)

if __name__ == "__main__":
    main()