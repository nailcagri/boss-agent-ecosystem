"""Entry point for the Boss Agent service.

This module wires together the registry (Postgres), queue (Redis), and
provides a tiny manager loop. It is intentionally minimal and safe:
- No secrets are committed here (config comes from environment)
- No irreversible actions are performed yet (only prints + status updates)

Next step after bootstrapping: add real tooling (API clients, Playwright
browser worker) and approval gates for sensitive actions.
"""

from __future__ import annotations

import time

from .config import Config
from .models import AuditEvent, TaskStatus
from .queue import dequeue_task, enqueue_task
from .registry import get_new_task_ids, insert_audit_events, update_task_status


AGENT_NAME = "boss"


def run_once(config: Config) -> int:
    """Process some NEW tasks once. Returns number processed."""
    new_task_ids = get_new_task_ids(config)
    if not new_task_ids:
        return 0

    # Put tasks on the queue (Boss can later decide which worker gets them)
    for task_id in new_task_ids:
        enqueue_task(config, task_id)

    processed = 0
    while True:
        task_id = dequeue_task(config)
        if task_id is None:
            break

        update_task_status(
            config,
            task_id,
            TaskStatus.IN_PROGRESS,
            assignee_agent=AGENT_NAME,
        )
        insert_audit_events(
            config,
            [
                AuditEvent(
                    agent_name=AGENT_NAME,
                    task_id=task_id,
                    action="started",
                    details="Boss accepted task",
                )
            ],
        )

        # Placeholder "execution"; replace with real tool calls.
        print(f"[boss] working on task {task_id}...")

        update_task_status(config, task_id, TaskStatus.DONE)
        insert_audit_events(
            config,
            [
                AuditEvent(
                    agent_name=AGENT_NAME,
                    task_id=task_id,
                    action="finished",
                    details="Boss marked task DONE",
                )
            ],
        )
        processed += 1

    return processed


def run() -> None:
    """Run the Boss Agent service."""
    config = Config()
    print("Boss agent online")

    while True:
        processed = run_once(config)
        if processed == 0:
            time.sleep(1.0)


if __name__ == "__main__":
    run()
