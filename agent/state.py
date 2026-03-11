from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


ISO_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class StateStore:
    """Persists lightweight agent metadata such as last sync timestamps."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load_last_sync(self) -> Optional[datetime]:
        if not self.path.exists():
            return None
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            value = payload.get("last_sync")
            if not value:
                return None
            return datetime.strptime(value, ISO_FORMAT)
        except Exception:
            return None

    def save_last_sync(self, moment: datetime) -> None:
        self.path.write_text(
            json.dumps({"last_sync": moment.strftime(ISO_FORMAT)}, indent=2),
            encoding="utf-8",
        )
