"""Named Facebook surface navigation primitives."""
from __future__ import annotations

from typing import Any

from .constants import SURFACE_GROUP, SURFACE_MARKETPLACE, SURFACE_MESSAGES
from .session import CamofoxSession


async def open_group(session: CamofoxSession, group_id: str, url: str | None = None) -> Any:
    return await session.open_surface(SURFACE_GROUP, {"group_id": group_id, "url": url})


async def open_messages(session: CamofoxSession, url: str | None = None) -> Any:
    return await session.open_surface(SURFACE_MESSAGES, {"url": url} if url else {})


async def open_marketplace(session: CamofoxSession, url: str | None = None) -> Any:
    return await session.open_surface(SURFACE_MARKETPLACE, {"url": url} if url else {})
