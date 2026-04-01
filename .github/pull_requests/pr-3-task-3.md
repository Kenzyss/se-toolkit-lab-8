# Pull Request #3 — Task 3: Give the Agent New Eyes

## Description

This PR implements Task 3: Give the Agent New Eyes. It builds MCP tools that let the agent query VictoriaLogs and VictoriaTraces, turning observability data into a conversational interface.

## Related Issue

Closes #3 (Task 3 — Give the Agent New Eyes)

## Changes

- Created `mcp/mcp_observability/` with log and trace tools:
  - `logs_search` — Search logs using LogsQL queries
  - `logs_error_count` — Count errors per service over a time window
  - `traces_list` — List recent traces for a service
  - `traces_get` — Fetch a specific trace by ID
- Created `nanobot/workspace/skills/observability/SKILL.md` with skill prompt
- Added observability MCP server to nanobot config
- Updated docker-compose.yml to include observability MCP service

## Acceptance Criteria

- [x] Agent can search backend error logs
- [x] Agent can fetch and analyze traces
- [x] Agent can summarize findings instead of dumping raw JSON

## Testing

Tested by:
- Stopping PostgreSQL and triggering a failure
- Asking agent "What went wrong?"
- Verifying agent uses both logs and traces to investigate

---

## Reviewer Checklist

- [ ] Code follows project conventions
- [ ] Changes are tested and working
- [ ] Documentation is updated

**Approval:** <!-- Reviewer: add your approval comment here -->
