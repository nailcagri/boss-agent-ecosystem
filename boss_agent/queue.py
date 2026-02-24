"""Redis-backed task queue.

The queue stores task IDs (ints) for worker assignment.
"""

from __future__ import annotations

from dataclasses import dataclass

import redis

from .config import Config

DEFAULT_QUEUE_KEY = "boss_agent:task_queue"


def client(config: Config) -> redis.Redis:
    return redis.from_url(config.REDIS_URL, decode_responses=True)


def enqueue_task(config: Config, task_id: int, queue_key: str = DEFAULT_QUEUE_KEY) -> None:
    client(config).lpush(queue_key, str(task_id))


def dequeue_task(config: Config, queue_key: str = DEFAULT_QUEUE_KEY) -> int | None:
    value = client(config).rpop(queue_key)
    return int(value) if value is not None else None


def queue_length(config: Config, queue_key: str = DEFAULT_QUEUE_KEY) -> int:
    return int(client(config).llen(queue_key))
