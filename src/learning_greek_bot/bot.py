from .config import TOKEN
from .core.bot_client import LearningGreekBot


def main() -> None:
    bot = LearningGreekBot()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
