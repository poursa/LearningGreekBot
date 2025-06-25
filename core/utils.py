from datetime import datetime, timedelta
import time
from discord import app_commands
from config import SYNC_DELAY_MINUTES, SYNC_TIMESTAMP_FILE


def should_sync():
    try:
        with open(SYNC_TIMESTAMP_FILE, 'r') as f:
            last = float(f.read())
        last_dt = datetime.fromtimestamp(last)
        return datetime.now() - last_dt > timedelta(minutes=SYNC_DELAY_MINUTES)
    except FileNotFoundError:
        return True


def update_sync_timestamp():
    with open(SYNC_TIMESTAMP_FILE, 'w') as f:
        f.write(str(time.time()))

def getcommand(self, attr: str) -> app_commands.Command | None:
    maybe_cmd = getattr(self, attr, None)
    if isinstance(maybe_cmd, app_commands.Command):
        return maybe_cmd
    return None