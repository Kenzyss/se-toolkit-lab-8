"""HTTP client for VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import httpx


class VictoriaLogsClient:
    """Client for VictoriaLogs HTTP API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def query(self, query: str, limit: int = 30, start: str = "1h") -> list[dict]:
        """Query VictoriaLogs using LogsQL."""
        url = f"{self.base_url}/select/logsql/query"
        params = {"query": query, "limit": limit, "start": start}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()


class VictoriaTracesClient:
    """Client for VictoriaTraces Jaeger API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def list_traces(self, service: str, limit: int = 10) -> list[dict]:
        """List traces for a service."""
        url = f"{self.base_url}/jaeger/api/traces"
        params = {"service": service, "limit": limit}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])

    async def get_trace(self, trace_id: str) -> dict | None:
        """Get a specific trace by ID."""
        url = f"{self.base_url}/jaeger/api/traces/{trace_id}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            traces = data.get("data", [])
            return traces[0] if traces else None
