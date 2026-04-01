# Observability Skill

You have access to observability tools for querying logs and traces in this system.

## Available Tools

### Logs (VictoriaLogs)

- **`logs_search`** — Search logs using LogsQL queries
  - `query`: LogsQL query string (e.g., `_stream:{service="backend"} AND level:error`)
  - `limit`: Max entries to return (default: 30)
  - `start`: Time window (e.g., "1h", "30m", "24h")

- **`logs_error_count`** — Count errors per service over a time window
  - `start`: Time window (e.g., "1h", "30m")

### Traces (VictoriaTraces)

- **`traces_list`** — List recent traces for a service
  - `service`: Service name (e.g., "backend")
  - `limit`: Max traces to return (default: 10)

- **`traces_get`** — Fetch a specific trace by ID
  - `trace_id`: The trace ID to fetch

## How to Use

### When the user asks "What went wrong?" or "Check system health"

**Follow this exact flow:**

1. **Search for recent errors first:**
   - Call `logs_error_count(start="10m")` to see which services have errors
   - If errors exist, call `logs_search(query="level:error", start="10m", limit=10)` to get details

2. **Extract trace ID from logs:**
   - Look for `trace_id=xxx` in the log entries
   - If found, note the trace ID

3. **Fetch the full trace:**
   - Call `traces_get(trace_id="xxx")` to see the complete span hierarchy
   - Identify which span failed (look for error markers or long durations)

4. **Summarize findings:**
   - What service failed
   - What error occurred (from logs)
   - Where in the request flow it failed (from trace)
   - Root cause hypothesis

**Example response structure:**
```
🔍 Investigation Summary

**Service:** Learning Management Service
**Error:** db_query failed: connection refused to PostgreSQL
**When:** 18:10:45

**Trace Analysis:**
- Trace ID: e067e1a90e24dd6776c2200a840f3cb0
- Failed span: db_query (app.db.items)
- Duration: 52ms before failure

**Root Cause:** PostgreSQL database is unavailable. All database queries are failing.

**Recommendation:** Restart PostgreSQL and verify health check passes.
```

### When the user asks about errors

1. First, use `logs_error_count` to see which services have errors
2. Then use `logs_search` to get details about specific errors
3. If you find a trace ID in the logs, fetch the full trace

### When the user asks "Any errors in the last hour?"

1. Call `logs_error_count` with `start="1h"`
2. If errors exist, call `logs_search` with `query="level:error"` and `start="1h"`
3. Summarize the findings concisely — don't dump raw JSON

### When the user asks about a specific service

1. Use `logs_search` with `query="_stream:{service=\"<name>\"}"`
2. For distributed issues, use `traces_list` to see recent traces

## Response Style

- Keep responses concise and actionable
- Format timestamps in human-readable form
- Highlight error messages clearly
- When showing traces, mention the span hierarchy and where errors occurred
- Don't dump raw JSON — summarize the key findings
- Use emojis sparingly for visual structure (🔍, ⚠️, ✅)

## Example Queries

**LogsQL examples:**
- `_stream:{service="backend"} AND level:error` — backend errors
- `message:"connection refused"` — search by message content
- `service="backend" | stats by (level) count()` — count by level

**Trace examples:**
- List traces: `traces_list(service="backend", limit=5)`
- Get trace: `traces_get(trace_id="abc123...")`
