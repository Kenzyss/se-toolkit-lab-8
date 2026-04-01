"""HTTP client for VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import json

import httpx


class VictoriaLogsClient:
    """Client for VictoriaLogs HTTP API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def query(self, query: str, limit: int = 30, start: str = "1h") -> list[dict]:
        """Query VictoriaLogs using LogsQL.
        
        VictoriaLogs returns JSONL (JSON Lines) format.
        """
        url = f"{self.base_url}/select/logsql/query"
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
                        continue
            return results


class VictoriaTracesClient:
    """Client for VictoriaTraces HTTP API.
    
    VictoriaTraces uses a different API than Jaeger.
    See: https://docs.victoriametrics.com/victoriatraces/
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def list_traces(self, service: str, limit: int = 10) -> list[dict]:
        """List traces for a service using VictoriaTraces API."""
        # VictoriaTraces API: GET /api/v1/traces?q=service:<name>&limit=<N>
        url = f"{self.base_url}/api/v1/traces"
        params = {"q": f"service:{service}", "limit": limit}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            # VictoriaTraces returns {"data": [...]} or [...] depending on version
            return data.get("data", data) if isinstance(data, dict) else data

    async def get_trace(self, trace_id: str) -> dict | None:
        """Get a specific trace by ID."""
        # VictoriaTraces API: GET /api/v1/traces/{trace_id}
        url = f"{self.base_url}/api/v1/traces/{trace_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data.get("data", data) if isinstance(data, dict) else data
