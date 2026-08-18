"""Messenger send action."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import MESSAGE_COMPOSER
from .compose import compose_message
from .schemas import SendMessageInput, SendMessageOutput
from .threads import open_thread


async def send_message(page: Any, data: SendMessageInput) -> SendMessageOutput:
    if data.thread_name and not await open_thread(page, data.thread_name):
        return SendMessageOutput(sent=False, thread_id=data.thread_id, error="thread_not_found")
    if not await compose_message(page, data.text):
        return SendMessageOutput(sent=False, thread_id=data.thread_id, error="composer_not_found")
    sent = await CamofoxInteractions(page).press(MESSAGE_COMPOSER, "Enter")
    return SendMessageOutput(
        sent=sent,
        thread_id=data.thread_id,
        error=None if sent else "send_failed",
    )
