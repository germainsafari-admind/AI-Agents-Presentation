from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List

from .config import Settings
from .formatter import build_blocks
from .scoro_client import ScoroClient
from .slack_client import SlackClient
from .state import StateStore


class TaskDigestAgent:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.scoro = ScoroClient(settings)
        self.slack = SlackClient(settings)
        self.state = StateStore(settings.state_file)

    def _get_window_start(self) -> datetime:
        last_sync = self.state.load_last_sync()
        if last_sync:
            return last_sync
        return datetime.now(timezone.utc) - timedelta(minutes=self.settings.sync_lookback_minutes)

    def run(self, dry_run: bool = False) -> List[dict]:
        window_start = self._get_window_start()
        tasks = self.scoro.fetch_tasks(window_start)
        blocks = build_blocks(tasks, window_start)
        if dry_run:
            return blocks
        self.slack.post_blocks(blocks)
        self.state.save_last_sync(datetime.now(timezone.utc))
        return blocks
