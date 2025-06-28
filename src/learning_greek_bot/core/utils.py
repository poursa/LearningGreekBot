from datetime import datetime, timedelta
import time
from discord import app_commands
from config import SYNC_DELAY_MINUTES, SYNC_TIMESTAMP_FILE
import re


def should_sync():
    try:
        last_str = SYNC_TIMESTAMP_FILE.read_text(encoding="utf-8").strip()
        last_dt = datetime.fromtimestamp(float(last_str))
        return datetime.now() - last_dt > timedelta(minutes=SYNC_DELAY_MINUTES)
    except FileNotFoundError:
        return True


def update_sync_timestamp():
    SYNC_TIMESTAMP_FILE.write_text(str(time.time()), encoding="utf-8")


def getcommand(self, attr: str) -> app_commands.Command | None:
    maybe_cmd = getattr(self, attr, None)
    if isinstance(maybe_cmd, app_commands.Command):
        return maybe_cmd
    return None


def sanitize_sentence(sentence):
    ### Remove mentions and links
    sentence = re.sub(r"<@!?[0-9]+>", "", sentence)
    sentence = re.sub(r"https?://\S+", "", sentence)
    return sentence
