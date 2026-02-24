"""Postgres-backed registry for agents, tasks, and audit logs."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

import psycopg

from .config import Config
from .models import AgentSpec, AuditEvent, TaskStatus


def _conn(config: Config) -> psycopg.Connection:
    return psycopg.connect(config.POSTGRES_URL)


def get_new_task_ids(config: Config, limit: int = 10) -> list[int]:
    """Return NEW tasks from task_inbox."""
    with _conn(config) as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM task_inbox
            WHERE status = 'NEW'
            ORDER BY created_at
            LIMIT %s
            """,
            (limit,),
        )
        return [row[0] for row in cur.fetchall()]


def update_task_status(
    config: Config,
    task_id: int,
    new_status: TaskStatus,
    assignee_agent: str | None = None,
    error: str | None = None,
) -> None:
    with _conn(config) as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE task_inbox
            SET status = %s,
                updated_at = NOW(),
                assignee_agent = COALESCE(%s, assignee_agent),
                error = %s
            WHERE id = %s
            """,
            (new_status.value, assignee_agent, error, task_id),
        )


def insert_audit_events(config: Config, events: Iterable[AuditEvent]) -> None:
    now = datetime.utcnow()
    with _conn(config) as conn, conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO audit_log
                (created_at, agent_name, task_id, action, details)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                now,
                event.agent_name,
                event.task_id,
                event.action,
                event.details,
            )
            for event in events
        )


def upsert_agent(config: Config, spec: AgentSpec) -> None:
    """Register or update an agent spec."""
    with _conn(config) as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_registry (name, role, allowed_tools, policy)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE
            SET role = EXCLUDED.role,
                allowed_tools = EXCLUDED.allowed_tools,
                policy = EXCLUDED.policy,
                updated_at = NOW()
            """,
            (
                spec.name,
                spec.role,
                list(spec.allowed_tools),
                spec.policy,
            ),
        )
