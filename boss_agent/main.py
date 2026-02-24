"""Entry point for the Boss Agent service.

This module wires together the agent registry, task inbox, and tool layer.
It is intentionally minimal so the Boss agent can evolve and generate
additional worker agents over time.

Next steps:
- Load configuration from environment
- Connect to Redis/Postgres
- Define tools (browser worker, APIs)
- Start the manager loop / API
"""

from __future__ import annotations


def run() -> None:
    """Run the Boss Agent service."""
    # TODO: implement manager loop
    raise NotImplementedError("Boss Agent run loop is not implemented yet")


if __name__ == "__main__":
    run()
