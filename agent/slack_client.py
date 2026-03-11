from __future__ import annotations

from typing import Iterable, List, Mapping, Optional

import requests

from .config import Settings


class SlackClient:
    """Minimal Slack Web API wrapper for posting agent updates."""

    def __init__(self, settings: Settings, session: Optional[requests.Session] = None) -> None:
        self.settings = settings
        self.session = session or requests.Session()

    def post_blocks(self, blocks: List[Mapping], targets: Optional[Iterable[str]] = None) -> None:
        channel_ids = list(targets) if targets else self.settings.slack_target_ids
        if not channel_ids:
            raise RuntimeError("No Slack targets configured")

        payload = {
            "blocks": blocks,
            "text": "Scoro task digest",
        }
        headers = {
            "Authorization": f"Bearer {self.settings.slack_bot_token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        url = "https://slack.com/api/chat.postMessage"
        for channel in channel_ids:
            body = {**payload, "channel": channel}
            response = self.session.post(url, headers=headers, json=body, timeout=15)
            response.raise_for_status()
            data = response.json()
            if not data.get("ok"):
                raise RuntimeError(f"Slack API error for {channel}: {data}")
