# Documentation Overview

This folder collects references for two audiences:

## 1. Product & API users
- **Public API guide** → `docs/public-api-guide.md`
  - Explains authentication, rate limits, endpoints, and sample responses for consumer apps and AI assistants that call the hosted API.
- **Deployment & operations** → `docs/deployment.md`
  - How to deploy on the Hetzner server, manage services, run health checks, and roll back.
- **General project README** → `../README.md`
  - Contains environment setup (frontend/backend), email + search infrastructure, and server operations.

## 2. AI agents / MCP integrations
- **MCP setup** → `docs/mcp-setup.md`
  - Describes each Model Context Protocol server (products, stores, analytics, etc.), env vars, and launch commands.
- **ChatGPT integration** → `docs/chatgpt-integration.md`
  - Step-by-step instructions for wiring the Partle MCP servers into ChatGPT’s Model Context Protocol feature.
- **Agent ground rules** → `../AGENTS.md`
  - Security policies, database constraints, and assistant-specific instructions that every AI client must follow.

### Quick pointers
- Hosted API base URL: `https://partle.rubenayla.xyz`
- AI API keys (read-only): `pk_test_chatgpt_readonly_key`, `pk_test_claude_readonly_key`
- MCP manifest location: `mcp-manifest.json` in the repository root

Keep these files in sync when infrastructure changes (API keys, MCP servers, Elasticsearch, etc.) so both humans and AI agents read consistent instructions.
