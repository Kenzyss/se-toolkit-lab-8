# Pull Request #1 — Task 1: Set Up the Agent

## Description

This PR implements Task 1: Set Up the Agent. It installs nanobot, configures the Qwen API connection, adds MCP tools for LMS integration, and writes the initial skill prompt.

## Related Issue

Closes #1 (Task 1 — Set Up the Agent)

## Changes

- Created `nanobot/config.json` with Qwen API configuration
- Added MCP server configuration for LMS tools
- Created `nanobot/workspace/skills/lms/SKILL.md` with skill prompt
- Updated docker-compose.yml to include nanobot service

## Acceptance Criteria

- [x] Agent can answer questions about available labs using MCP tools
- [x] Agent knows when to ask for a lab parameter
- [x] Agent formats numeric results correctly (percentages, counts)

## Testing

Tested by asking the agent:
- "What labs are available?" — correctly lists all 8 labs
- "Show me the scores" — correctly queries LMS API and formats results

---

## Reviewer Checklist

- [ ] Code follows project conventions
- [ ] Changes are tested and working
- [ ] Documentation is updated

**Approval:** <!-- Reviewer: add your approval comment here -->
