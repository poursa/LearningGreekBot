import re
import time
from datetime import datetime, timedelta

from ..config import SYNC_DELAY_MINUTES, SYNC_TIMESTAMP_FILE


def should_sync():
    try:
        last_str = SYNC_TIMESTAMP_FILE.read_text(encoding="utf-8").strip()
        last_dt = datetime.fromtimestamp(float(last_str))
        return datetime.now() - last_dt > timedelta(minutes=SYNC_DELAY_MINUTES)
    except FileNotFoundError:
        return True


def update_sync_timestamp() -> None:
    SYNC_TIMESTAMP_FILE.parent.mkdir(parents=True, exist_ok=True)
    SYNC_TIMESTAMP_FILE.write_text(str(time.time()), encoding="utf-8")


def sanitize_sentence(sentence: str) -> str:
    ### Remove mentions and links
    sentence = re.sub(r"<@!?[0-9]+>", "", sentence)
    sentence = re.sub(r"https?://\S+", "", sentence)
    return sentence
