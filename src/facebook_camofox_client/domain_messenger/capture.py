"""Messenger capture action combining thread discovery and message reads."""
from __future__ import annotations

from typing import Any

from .messages import read_messages
from .threads import list_threads, open_thread


async def capture_threads(page: Any, limit: int = 50) -> dict:
    threads = await list_threads(page, limit=limit)
    return {"threads": [thread.model_dump() for thread in threads]}


async def capture_thread(page: Any, thread_name: str, limit: int = 100) -> dict:
    if not await open_thread(page, thread_name):
        return {"messages": [], "error": "thread_not_found"}
    messages = await read_messages(page, limit=limit)
    return {"messages": [message.model_dump() for message in messages]}
