"""Messenger surface opening."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.constants import SURFACE_MESSAGES


async def open_messages(session: Any, url: str | None = None) -> Any:
    return await session.open_surface(SURFACE_MESSAGES, {"url": url} if url else {})
