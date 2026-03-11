from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from .config import Settings


class ScoroClient:
    """Lightweight wrapper around the Scoro REST API."""

    def __init__(self, settings: Settings, session: Optional[requests.Session] = None) -> None:
        self.settings = settings
        self.session = session or requests.Session()
        self._access_token: Optional[str] = settings.scoro_auth_token

    @property
    def _base_url(self) -> str:
        return f"{self.settings.scoro_base_url}/api/v2"

    def _ensure_token(self) -> str:
        if self._access_token:
            return self._access_token

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.settings.scoro_client_id,
            "client_secret": self.settings.scoro_client_secret,
            "scope": "tasks.read"
        }
        response = self.session.post(f"{self._base_url}/oauth/token", data=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        self._access_token = data.get("access_token")
        if not self._access_token:
            raise RuntimeError("Scoro auth response did not include an access_token")
        return self._access_token

    def fetch_tasks(self, modified_after: datetime) -> List[Dict[str, Any]]:
        token = self._ensure_token()
        params = {
            "company_account": self.settings.scoro_company_account,
            "modified_since": modified_after.isoformat(),
            "status": "not_done",
            "per_page": 100,
            "page": 1,
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        tasks: List[Dict[str, Any]] = []
        while True:
            response = self.session.get(
                f"{self._base_url}/tasks",
                headers=headers,
                params=params,
                timeout=20,
            )
            response.raise_for_status()
            payload = response.json()
            items = payload.get("data", [])
            tasks.extend(items)
            if not payload.get("next_page"):
                break
            params["page"] += 1
        return tasks
