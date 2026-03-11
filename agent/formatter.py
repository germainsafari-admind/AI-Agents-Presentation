from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def _deadline_status(task: Dict[str, Any]) -> str:
    deadline = _parse_datetime(task.get("deadline"))
    if not deadline:
        return "unscheduled"
    now = datetime.now(timezone.utc)
    if deadline < now:
        return "overdue"
    if deadline - now <= timedelta(days=2):
        return "due_soon"
    return "scheduled"


def summarize(tasks: Iterable[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"total": 0, "overdue": 0, "due_soon": 0, "unscheduled": 0}
    for task in tasks:
        counts["total"] += 1
        status = _deadline_status(task)
        counts[status] = counts.get(status, 0) + 1
    return counts


def build_blocks(tasks: List[Dict[str, Any]], window_start: datetime) -> List[Dict[str, Any]]:
    counts = summarize(tasks)
    header = {
        "type": "header",
        "text": {"type": "plain_text", "text": "Scoro Task Digest"},
    }
    summary = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                f"*Window:* since {window_start.strftime('%Y-%m-%d %H:%M UTC')}\n"
                f"• Total tasks reviewed: *{counts['total']}*\n"
                f"• Overdue: *{counts.get('overdue', 0)}* | Due soon (<48h): *{counts.get('due_soon', 0)}*"
            ),
        },
    }

    if not tasks:
        return [header, summary, {"type": "section", "text": {"type": "mrkdwn", "text": "No task changes detected."}}]

    bullets = []
    for task in tasks[:5]:
        title = task.get("title") or task.get("name") or "Untitled"
        assignee = task.get("assignee", {}).get("name") or "Unassigned"
        status = task.get("status", {}).get("name") or task.get("status") or "n/a"
        deadline = task.get("deadline")
        deadline_text = _parse_datetime(deadline)
        deadline_fmt = deadline_text.strftime("%d %b %H:%M") if deadline_text else "—"
        url = task.get("url") or task.get("permalink")
        line = f"• *{title}* ({status}) — {assignee}, due {deadline_fmt}"
        if url:
            line += f" → <{url}|open>"
        bullets.append(line)

    details = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "\n".join(bullets)},
    }
    return [header, summary, details]
