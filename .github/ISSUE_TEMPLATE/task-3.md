---
name: Task 3 — Give the Agent New Eyes
about: Explore observability data, write log/trace MCP tools
title: 'Task 3: Give the Agent New Eyes'
labels: 'task-3'
assignees: ''
---

## Description

Build MCP tools that let the agent query VictoriaLogs and VictoriaTraces, turning observability data into a conversational interface.

## Deliverables

- [ ] VictoriaLogs MCP tool (`logs_search`, `logs_error_count`)
- [ ] VictoriaTraces MCP tool (`traces_list`, `traces_get`)
- [ ] Observability skill prompt in `nanobot/workspace/skills/observability/SKILL.md`
- [ ] MCP servers registered in nanobot config

## Acceptance Criteria

- [ ] Agent can search backend error logs
- [ ] Agent can fetch and analyze traces
- [ ] Agent can summarize findings instead of dumping raw JSON
