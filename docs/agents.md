# AI Assistant Guide

This is a summary for any AI agent or MCP client that interacts with Partle. For the full rulebook see [`AGENTS.md`](../AGENTS.md).

!!! warning "MCP tools still experimental"
    The MCP servers, ChatGPT integration, and other AI tooling are being prototyped. Validate every workflow manually before relying on automated interactions.

## Ground rules
- **Single production database**: `postgresql://partle_user@91.98.68.236:5432/partle`. Never create or migrate against local databases unless explicitly told.
- **Secrets** live in per-service `.env` files (`backend/.env`, `frontend/.env`). Do not invent new environment variables without approval.
- **Authentication UX**: one combined login/signup endpoint (`/v1/auth/login`). Never add separate pages or flows.
- **Ports**: frontend dev on 3000, backend on 8000, Postgres 5432, Elasticsearch 9200.

## Assisted workflows
- Trigger the React search bar and layout only from `Layout.tsx` (one global instance).
- `SearchBar` controls are fixed at top; mobile vs. desktop components should not be duplicated.
- When building scripts/tests, run `npm run build` for the frontend and `uv run python -c "from app.main import app"` for backend sanity checks.

## Incident response
- Credential exposure requires immediate rotation and notification (see `AGENTS.md` for the full procedure). Last incident: 2025‑09‑05 when `backend/downloaded_server.env` was committed.

## MCP / AI integrations
- Local MCP scripts live in `backend/scripts/run_mcp_*.py`.
- Configure ChatGPT/Claude using the `mcp-manifest.json` in the repo root or follow `docs/mcp-setup.md`.

🛈 Always review `AGENTS.md` before making automated changes; this page just highlights the most critical constraints.
