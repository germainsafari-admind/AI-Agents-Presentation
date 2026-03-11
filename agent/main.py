from __future__ import annotations

import argparse
import json

from .agent import TaskDigestAgent
from .config import MissingSettingError, load_settings


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scoro → Slack task digest agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch tasks and print Slack payload without posting",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        settings = load_settings()
    except MissingSettingError as exc:
        parser.error(str(exc))

    agent = TaskDigestAgent(settings)
    blocks = agent.run(dry_run=args.dry_run)
    if args.dry_run:
        print(json.dumps(blocks, indent=2))


if __name__ == "__main__":
    main()
