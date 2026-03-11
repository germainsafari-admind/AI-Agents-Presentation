from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    scoro_base_url: str
    scoro_client_id: str
    scoro_client_secret: str
    scoro_auth_token: Optional[str]
    scoro_company_account: str
    slack_bot_token: str
    slack_target_ids: List[str]
    sync_lookback_minutes: int
    state_file: Path


class MissingSettingError(RuntimeError):
    """Raised when required environment variables are absent."""


REQUIRED_KEYS = [
    "SCORO_BASE_URL",
    "SCORO_CLIENT_ID",
    "SCORO_CLIENT_SECRET",
    "SCORO_COMPANY_ACCOUNT",
    "SLACK_BOT_TOKEN",
]


OPTIONAL_DEFAULTS = {
    "SYNC_LOOKBACK_MINUTES": "120",
    "STATE_FILE": ".agent_state.json",
}


def _get_env(key: str) -> Optional[str]:
    value = os.getenv(key)
    if value is None and key in OPTIONAL_DEFAULTS:
        value = OPTIONAL_DEFAULTS[key]
    return value


def load_settings() -> Settings:
    missing = [key for key in REQUIRED_KEYS if not os.getenv(key)]
    if missing:
        raise MissingSettingError(
            "Missing required settings: " + ", ".join(sorted(missing))
        )

    target_ids = [item.strip() for item in os.getenv("SLACK_TARGET_IDS", "").split(",") if item.strip()]

    return Settings(
        scoro_base_url=os.environ["SCORO_BASE_URL"].rstrip("/"),
        scoro_client_id=os.environ["SCORO_CLIENT_ID"],
        scoro_client_secret=os.environ["SCORO_CLIENT_SECRET"],
        scoro_auth_token=_get_env("SCORO_AUTH_TOKEN"),
        scoro_company_account=os.environ["SCORO_COMPANY_ACCOUNT"],
        slack_bot_token=os.environ["SLACK_BOT_TOKEN"],
        slack_target_ids=target_ids,
        sync_lookback_minutes=int(_get_env("SYNC_LOOKBACK_MINUTES") or 120),
        state_file=Path(_get_env("STATE_FILE") or ".agent_state.json"),
    )
