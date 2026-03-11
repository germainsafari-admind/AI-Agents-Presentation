# AI Agents Presentation

This repository now includes a working scaffold for a Scoro → Slack digest agent alongside the presentation notes. Use it as a reference implementation when demonstrating how AI agents can automate cross-tool workflows.

## Features
- Fetches Scoro tasks updated since the last run (or a configurable lookback window)
- Summarizes overdue and soon-due tasks into Slack Block Kit messages
- Posts digests to specific Slack channels or DMs
- Persists last sync timestamp locally to avoid duplicate notifications
- Ships with `.env` scaffolding plus safe defaults in code

## Getting Started
1. **Install dependencies**
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Configure secrets**
   - Copy `.env.example` to `.env`
   - Fill in Scoro and Slack credentials (never commit `.env`)
   - Share your Scoro integration with the relevant company account
3. **Run the agent**
   ```bash
   python -m agent.main --dry-run   # prints Slack payload
   python -m agent.main             # posts to Slack
   ```

## Repository Layout
```
agent/
  config.py        # loads environment variables and validation
  scoro_client.py  # minimal REST wrapper for Scoro tasks
  slack_client.py  # Slack Web API helper
  formatter.py     # builds Slack Block Kit messages
  state.py         # last-sync persistence
  agent.py         # orchestration logic
  main.py          # CLI entrypoint
```

## Next Improvements
- Add unit tests with mocked Scoro/Slack responses
- Support per-user digests (one Slack DM per assignee)
- Wire this agent into a GitHub Actions workflow or hosted worker
- Store state in Redis/Postgres for multi-instance deployments
