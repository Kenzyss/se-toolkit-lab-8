---
name: Task 4 — Diagnose a Failure and Make the Agent Proactive
about: Investigate a failure, schedule health checks, fix a planted bug
title: 'Task 4: Diagnose a Failure and Make the Agent Proactive'
labels: 'task-4'
assignees: ''
---

## Description

Use the agent to investigate a backend failure, schedule proactive health checks via cron, and fix a planted bug that returns 404 instead of 500 on database failures.

## Deliverables

- [ ] Observability skill enhanced for one-shot investigation
- [ ] Agent can investigate "What went wrong?" using logs + traces
- [ ] Scheduled health check job created via cron tool
- [ ] Planted bug fixed (DB failure returns 500, not 404)
- [ ] Bug fix verified with agent investigation

## Acceptance Criteria

- [ ] Agent response to "What went wrong?" includes both log and trace evidence
- [ ] Health check job appears in "List scheduled jobs"
- [ ] Proactive health report posted to chat while failure is present
- [ ] After fix, DB failure returns proper 500 error
- [ ] Post-recovery health report shows system healthy
