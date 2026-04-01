#!/usr/bin/env python3
"""
Entrypoint for nanobot Docker container.

Resolves environment variables into config.json at runtime,
then launches nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def main():
    # Paths
    nanobot_dir = Path("/app/nanobot")
    config_path = nanobot_dir / "config.json"
    resolved_path = nanobot_dir / "config.resolved.json"
    workspace_dir = nanobot_dir / "workspace"

    # Read base config
    with open(config_path) as f:
        config = json.load(f)

    # Resolve LLM provider config from env vars
    config["providers"]["custom"]["apiKey"] = os.environ.get(
        "LLM_API_KEY", config["providers"]["custom"].get("apiKey", "")
    )
    config["providers"]["custom"]["apiBase"] = os.environ.get(
        "LLM_API_BASE_URL", config["providers"]["custom"].get("apiBase", "")
    )

    # Resolve MCP server env vars
    if "mcpServers" in config.get("tools", {}):
        if "lms" in config["tools"]["mcpServers"]:
            config["tools"]["mcpServers"]["lms"]["env"] = {
                "NANOBOT_LMS_BACKEND_URL": os.environ.get(
                    "NANOBOT_LMS_BACKEND_URL",
                    config["tools"]["mcpServers"]["lms"]["env"].get(
                        "NANOBOT_LMS_BACKEND_URL", ""
                    ),
                ),
                "NANOBOT_LMS_API_KEY": os.environ.get(
                    "NANOBOT_LMS_API_KEY",
                    config["tools"]["mcpServers"]["lms"]["env"].get(
                        "NANOBOT_LMS_API_KEY", ""
                    ),
                ),
            }

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"[entrypoint] Resolved config written to {resolved_path}", file=sys.stderr)

    # Launch nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            str(workspace_dir),
        ],
    )


if __name__ == "__main__":
    main()
