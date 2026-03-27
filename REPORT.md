# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### "What is the agentic loop?"

The agentic loop is the core reasoning cycle that enables AI agents to act autonomously. It's a continuous feedback loop:

```
┌─────────────────────────────────────────┐
│  1. PERCEIVE  →  2. REASON  →  3. ACT  │
│       ↑                              │  │
│       └────── 4. OBSERVE ←───────────┘  │
└─────────────────────────────────────────┘
```

| Step        | What Happens                                      |
|-------------|---------------------------------------------------|
| 1. Perceive | Gather input (user request, tool outputs, etc.)   |
| 2. Reason   | Analyze, plan, decide next actions                |
| 3. Act      | Execute tools, send messages, modify state        |
| 4. Observe  | Receive feedback from actions (results, errors)   |

Then the loop repeats until the goal is achieved.

**Example (What the agent just did):**
When asked "What labs are available?":
1. Perceive: Understood the question
2. Reason: Decided to call the LMS API
3. Act: Called `mcp_lms_labs`
4. Observe: Got the list of labs
5. Reason: Formatted the response
6. Act: Showed the results

### "What labs are available in our LMS?" (without tools)

Without MCP tools, the agent doesn't know about the LMS and would hallucinate or say it doesn't know. It might search the local filesystem and find lab folders, but cannot access real LMS data.

## Task 1B — Agent with LMS tools

### "What labs are available?"

With MCP tools configured, the agent returns real lab names from the backend:

```
Great! The LMS is now online. Here are the 8 available labs:

 #  Lab ID  Title                                    Description
 ───────────────────────────────────────────────────────────────
 1  lab-01  Introduction to Git and Market Analysis
 2  lab-02  Linux Basics and Shell Scripting
 3  lab-03  Python and Package Management
 4  lab-04  Docker and Containerization
 5  lab-05  Web API Development
 6  lab-06  LLM Tool Calling
 7  lab-07  Telegram Bot Development
 8  lab-08  Nanobot Agent Framework
```

### "Describe the architecture of the LMS system"

The LMS architecture consists of:

**1. Backend API (FastAPI + PostgreSQL)**
- REST API with endpoints: `/items`, `/learners`, `/analytics/*`, `/pipeline/sync`
- PostgreSQL database with tables: `item`, `learner`, `interacts`
- ETL pipeline to sync data from external autochecker API

**2. MCP Server (mcp/mcp_lms/)**
- Exposes LMS API as typed tools: `lms_health`, `lms_labs`, `lms_pass_rates`, etc.
- Uses stdio transport protocol
- Any MCP-compatible agent can use these tools

**3. LLM Gateway (qwen-code-api/)**
- OpenAI-compatible proxy for Qwen API
- Handles authentication, rate limiting, retries
- Default model: `coder-model`

**4. Nanobot Agent**
- Framework-based agent loop (no manual tool-calling code)
- Connects to MCP server for LMS tools
- Supports multiple channels (WebSocket, Telegram, etc.)

**5. Observability Stack**
- OpenTelemetry Collector (gRPC port 4317)
- VictoriaLogs for log storage
- VictoriaTraces for distributed tracing

**6. Reverse Proxy (Caddy)**
- Single entry point on port 42002
- Routes traffic to backend, web clients, observability UIs

## Task 1C — Skill prompt

### "Show me the scores" (without specifying a lab)

With the skill prompt at `nanobot/workspace/skills/lms/SKILL.md`, the agent now:
1. Asks which lab the user wants to see (as instructed in the skill)
2. OR provides a summary of all labs if it decides to be helpful

**Agent response:**

```
LMS Scores Summary

The LMS is healthy and connected, but currently shows no student data:

 Lab     Title                                    Completion Rate  Passed  Total Students
 ────────────────────────────────────────────────────────────────────────────────────────
 lab-01  Introduction to Git and Market Analysis  0%               0       0
 lab-02  Linux Basics and Shell Scripting         0%               0       0
 lab-03  Python and Package Management            0%               0       0
 lab-04  Docker and Containerization              0%               0       0
 lab-05  Web API Development                      0%               0       0
 lab-06  LLM Tool Calling                         0%               0       0
 lab-07  Telegram Bot Development                 0%               0       0
 lab-08  Nanobot Agent Framework                  0%               0       0

Status: The LMS appears to be a fresh instance with no learners registered and no submissions yet.

Would you like me to:
 1 Trigger the sync pipeline to pull in any pending data?
 2 Check group performance for a specific lab?
 3 View the submission timeline for any lab?
```

### Skill Prompt Created

File: `nanobot/workspace/skills/lms/SKILL.md`

The skill prompt teaches the agent:
- Which `lms_*` tools are available and when to use each one
- When a lab parameter is needed but not provided, ask the user which lab (or list available labs)
- Format numeric results nicely (percentages with one decimal, counts)
- Keep responses concise and actionable
- When asked "what can you do?", explain current tools and limits clearly

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
