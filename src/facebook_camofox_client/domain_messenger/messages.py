"""Messenger message extraction and normalization."""
from __future__ import annotations

from typing import Any

from .schemas import Message


async def read_messages(page: Any, limit: int = 100) -> list[Message]:
    candidates = [
        "[data-scope='messages_table'] [role='gridcell']",
        "[role='main'] [role='gridcell']",
    ]
    locator = None
    for selector in candidates:
        candidate = page.locator(selector)
        if await candidate.count() > 0:
            locator = candidate
            break
    if locator is None:
        return []

    count = min(await locator.count(), limit)
    results: list[Message] = []
    for index in range(count):
        item = locator.nth(index)
        try:
            text = (await item.inner_text()).strip()
        except Exception:
            continue
        if not text:
            continue
        results.append(Message(text=text, direction="unknown"))
    return results
