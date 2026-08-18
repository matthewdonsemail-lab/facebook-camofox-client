"""Camofox session object and Facebook surface routing."""
from __future__ import annotations

import uuid
from typing import Any

from .constants import (
    FACEBOOK_BASE_URL,
    FACEBOOK_MARKETPLACE_CREATE_URL,
    FACEBOOK_MESSAGES_URL,
    SUPPORTED_SURFACES,
    SURFACE_GROUP,
    SURFACE_MARKETPLACE,
    SURFACE_MESSAGES,
)


class CamofoxSession:
    def __init__(self, account_id: str, runtime: Any, browser: Any, context: Any) -> None:
        self.account_id = account_id
        self.session_id = str(uuid.uuid4())
        self.runtime = runtime
        self.browser = browser
        self.context = context
        self._closed = False

    async def new_page(self) -> Any:
        return await self.context.new_page()

    async def open_surface(self, surface: str, target: dict[str, Any] | None = None) -> Any:
        target = target or {}
        if surface not in SUPPORTED_SURFACES:
            raise ValueError(f"unsupported surface: {surface}")
        if surface == SURFACE_GROUP:
            url = target.get("url") or f"{FACEBOOK_BASE_URL}/groups/{target['group_id']}"
        elif surface == SURFACE_MESSAGES:
            url = target.get("url") or FACEBOOK_MESSAGES_URL
        elif surface == SURFACE_MARKETPLACE:
            url = target.get("url") or FACEBOOK_MARKETPLACE_CREATE_URL
        else:
            raise ValueError(f"unsupported surface: {surface}")
        page = await self.context.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        return page

    async def execute(self, activity: str, params: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError(f"Camofox activity is not registered: {activity}")
