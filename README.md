# Boss Agent Ecosystem

Meta-agent (the **Boss**) orchestrates work 24/7, builds/updates worker agents (agent factory), and executes actions via controlled tools.

## Stack (planned)
- **LangGraph** orchestrator (state/routing/retries)
- **Redis** task queue
- **Postgres** memory + audit logs + agent registry
- **Playwright** browser worker
- Optional **OpenWebUI** as supervisor/control panel

## Quick start (planned)
1. Fill `.env` files (API keys, DB creds)
2. `docker compose up -d`
3. Boss watches the task inbox and routes jobs

## Repository layout (planned)
```
/infra
  docker-compose.yml
  init-postgres.sql
/services
  boss-agent/
  browser-worker/
  worker-template/
/docs
  roadmap.md
  guardrails.md
```
