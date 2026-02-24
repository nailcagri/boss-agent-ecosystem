from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    NEEDS_APPROVAL = "NEEDS_APPROVAL"
    DONE = "DONE"
    FAILED = "FAILED"


class AgentSpec(BaseModel):
    """Definition for a worker agent created by the Boss."""

    name: str
    role: str
    description: str
    tools: list[str] = Field(default_factory=list)
    policy: str = Field(
        default="", description="Plain-language rules the agent must follow."
    )
    version: int = 1


class Task(BaseModel):
    id: int
    title: str
    payload: dict[str, Any]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    assigned_agent: str | None = None


class AuditLog(BaseModel):
    id: int
    actor: str
    action: str
    target: str
    outcome: Literal["SUCCESS", "FAILURE"]
    details: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
