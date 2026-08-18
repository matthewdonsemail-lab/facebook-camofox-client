from __future__ import annotations

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        pytest.fail(f"Missing required runtime environment variable: {name}")
    return value


@pytest.fixture(scope="session")
def runtime_config() -> dict[str, str | None]:
    enabled = os.getenv("FACEBOOK_RUNTIME_ENABLED", "false").lower() == "true"
    if not enabled:
        pytest.fail("FACEBOOK_RUNTIME_ENABLED=true is required for client runtime tests")

    return {
        "account_id": _required("FACEBOOK_ACCOUNT_ID"),
        "email": _required("FACEBOOK_EMAIL"),
        "password": _required("FACEBOOK_PASSWORD"),
        "totp_secret": os.getenv("FACEBOOK_TOTP_SECRET"),
        "proxy_server": os.getenv("FACEBOOK_PROXY_SERVER"),
        "proxy_username": os.getenv("FACEBOOK_PROXY_USERNAME"),
        "proxy_password": os.getenv("FACEBOOK_PROXY_PASSWORD"),
        "storage_state_path": os.getenv("FACEBOOK_STORAGE_STATE_PATH"),
    }
