"""Observability MCP server exposing VictoriaLogs and VictoriaTraces as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("observability")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_logs_url: str = ""
_traces_url: str = ""


def _get_logs_url() -> str:
    return os.environ.get("VICTORIALOGS_URL", "http://localhost:9428")


def _get_traces_url() -> str:
    return os.environ.get("VICTORIATRACES_URL", "http://localhost:10428")


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _LogsSearchArgs(BaseModel):
    query: str = Field(
        default="_stream:{service=\"backend\"}",
        description="LogsQL query string. Example: '_stream:{service=\"backend\"} AND level:error'",
    )
    limit: int = Field(default=30, ge=1, le=1000, description="Max log entries to return")
    start: str = Field(
        default="1h",
        description="Start time for the query (e.g., '1h', '30m', '24h'). Default: 1h",
    )


class _LogsErrorCountArgs(BaseModel):
    start: str = Field(default="1h", description="Time window to search (e.g., '1h', '30m')")


class _TracesListArgs(BaseModel):
    service: str = Field(default="backend", description="Service name to search traces for")
    limit: int = Field(default=10, ge=1, le=100, description="Max traces to return")


class _TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _query_victorialogs(query: str, limit: int = 30, start: str = "1h") -> list[dict]:
    """Query VictoriaLogs using LogsQL.
    
    VictoriaLogs returns JSONL (JSON Lines) format, not pure JSON.
    Each line is a separate JSON object.
    """
    url = f"{_logs_url}/select/logsql/query"
    params = {"query": query, "limit": limit, "start": start}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        text = response.text.strip()
        if not text:
            return []
        # Parse JSONL format (each line is a JSON object)
        results = []
        for line in text.split('\n'):
            line = line.strip()
            if line:
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    # Skip malformed lines
                    continue
        return results


async def _query_victoriatraces_traces(service: str, limit: int = 10) -> list[dict]:
    """List traces from VictoriaTraces Jaeger API."""
    url = f"{_traces_url}/jaeger/api/traces"
    params = {"service": service, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])


async def _get_trace(trace_id: str) -> dict | None:
    """Get a specific trace by ID."""
    url = f"{_traces_url}/jaeger/api/traces/{trace_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        traces = data.get("data", [])
        return traces[0] if traces else None


def _text(data: Any) -> list[TextContent]:
    """Serialize data to JSON text."""
    return [TextContent(type="text", text=json.dumps(data, indent=2, ensure_ascii=False))]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsSearchArgs) -> list[TextContent]:
    """Search logs using LogsQL."""
    try:
        results = await _query_victorialogs(args.query, args.limit, args.start)
        return _text(results)
    except httpx.HTTPError as e:
        return _text({"error": f"VictoriaLogs query failed: {e}"})
    except Exception as e:
        return _text({"error": f"Error: {type(e).__name__}: {e}"})


async def _logs_error_count(args: _LogsErrorCountArgs) -> list[TextContent]:
    """Count errors per service over a time window.
    
    VictoriaLogs LogsQL syntax: `level:error | stats by (field) count()`
    Returns empty list if no errors found (which is a valid healthy state).
    """
    query = f'level:error | stats by (service) count()'
    try:
        results = await _query_victorialogs(query, limit=100, start=args.start)
        # Empty results = no errors found (healthy state)
        if not results:
            return _text({
                "status": "healthy",
                "message": "No errors found in the specified time window",
                "time_window": args.start,
                "error_count": 0,
            })
        return _text(results)
    except httpx.HTTPError as e:
        return _text({"error": f"VictoriaLogs query failed: {e}"})
    except Exception as e:
        return _text({"error": f"Error: {type(e).__name__}: {e}"})


async def _traces_list(args: _TracesListArgs) -> list[TextContent]:
    """List recent traces for a service."""
    try:
        traces = await _query_victoriatraces_traces(args.service, args.limit)
        summary = []
        for trace in traces[:10]:
            summary.append({
                "trace_id": trace.get("traceID"),
                "spans": len(trace.get("spans", [])),
                "start_time": trace.get("startTime"),
                "duration": trace.get("duration"),
            })
        return _text({"traces": summary, "total": len(traces)})
    except httpx.HTTPError as e:
        return _text({"error": f"VictoriaTraces query failed: {e}"})
    except Exception as e:
        return _text({"error": f"Error: {type(e).__name__}: {e}"})


async def _traces_get(args: _TracesGetArgs) -> list[TextContent]:
    """Get a specific trace by ID."""
    try:
        trace = await _get_trace(args.trace_id)
        if trace:
            return _text(trace)
        return _text({"error": f"Trace not found: {args.trace_id}"})
    except httpx.HTTPError as e:
        return _text({"error": f"VictoriaTraces query failed: {e}"})
    except Exception as e:
        return _text({"error": f"Error: {type(e).__name__}: {e}"})


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (model, handler, Tool(name=name, description=description, inputSchema=schema))


_register(
    "logs_search",
    "Search VictoriaLogs using LogsQL. Returns log entries matching the query.",
    _LogsSearchArgs,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count errors per service over a time window. Use to find which services have errors.",
    _LogsErrorCountArgs,
    _logs_error_count,
)
_register(
    "traces_list",
    "List recent traces for a service. Returns trace IDs and basic info.",
    _TracesListArgs,
    _traces_list,
)
_register(
    "traces_get",
    "Get a specific trace by ID. Returns full trace with all spans.",
    _TracesGetArgs,
    _traces_get,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    global _logs_url, _traces_url
    _logs_url = _get_logs_url()
    _traces_url = _get_traces_url()
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
