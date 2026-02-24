from __future__ import annotations

import os
from dataclasses import dataclass


def _env(key: str, default: str | None = None) -> str:
    value = os.getenv(key)
    if value:
        return value
    if default is not None:
        return default
    raise RuntimeError(f"Missing required env var: {key}")


@dataclass(slots=True)
class Config:
    redis_url: str
    postgres_url: str
    browser_worker_url: str | None
    auto_approve: bool


def load_config() -> Config:
    return Config(
        redis_url=_env("REDIS_URL"),
        postgres_url=_env("POSTGRES_URL"),
        browser_worker_url=os.getenv("BROWSER_WORKER_URL"),
        auto_approve=os.getenv("AUTO_APPROVE", "false").lower() in {"1", "true", "yes", "y"},
    )
