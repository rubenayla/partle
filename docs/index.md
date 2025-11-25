# Documentation Overview

Use this portal as the canonical reference for operations, APIs, and AI tooling.

## Product & API users
- [Public API guide](public-api-guide.md) – authentication, rate limits, and sample requests for consumer integrations and AI agents that hit the hosted API.
- [Deployment & operations](deployment.md) – Hetzner server layout, deploy scripts, health checks, and rollback procedures.
- Main project [README](../README.md) – local dev setup, email/search infrastructure, and codebase layout.

## AI agents & MCP integrations
- [MCP setup](mcp-setup.md) – details for each Model Context Protocol server (products, stores, analytics, etc.) and the required environment variables.
- [ChatGPT integration](chatgpt-integration.md) – how to expose the MCP servers to ChatGPT’s Model Context Protocol UI.
- [Agent guide](agents.md) – condensed guardrails; the full policy still lives in `AGENTS.md` at the repo root.

### Quick pointers
- Hosted API base URL: `https://partle.rubenayla.xyz`
- Read‑only API keys: `pk_test_chatgpt_readonly_key`, `pk_test_claude_readonly_key`
- MCP manifest: `mcp-manifest.json` at the repo root

Keep these docs in sync whenever infrastructure (API keys, MCP servers, Elasticsearch, etc.) changes so both humans and AI assistants have a single source of truth.
