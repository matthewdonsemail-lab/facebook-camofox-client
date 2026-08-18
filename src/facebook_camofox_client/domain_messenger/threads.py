"""Messenger thread discovery primitives."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import MESSAGE_THREAD_LINKS
from .schemas import Thread


async def list_threads(page: Any, limit: int = 50) -> list[Thread]:
    locator = page.locator(MESSAGE_THREAD_LINKS[0])
    count = min(await locator.count(), limit)
    results: list[Thread] = []
    seen: set[str] = set()
    for index in range(count):
        item = locator.nth(index)
        try:
            href = await item.get_attribute("href")
            name = (await item.inner_text()).strip()
        except Exception:
            continue
        if not href or not name or href in seen:
            continue
        seen.add(href)
        thread_id = href.rstrip("/").split("/")[-1]
        results.append(Thread(thread_id=thread_id, name=name))
    return results


async def open_thread(page: Any, thread_name: str) -> bool:
    locator = page.locator(MESSAGE_THREAD_LINKS[0])
    count = await locator.count()
    for index in range(count):
        item = locator.nth(index)
        try:
            if (await item.inner_text()).strip() == thread_name:
                await item.click()
                return True
        except Exception:
            continue
    return False
