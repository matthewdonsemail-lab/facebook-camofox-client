"""Messenger send action."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import MESSAGE_COMPOSER
from .compose import compose_message
from .schemas import SendMessageInput, SendMessageOutput


async def send_message(page: Any, data: SendMessageInput) -> SendMessageOutput:
    if not await compose_message(page, data.text):
        return SendMessageOutput(sent=False, thread_id=data.thread_id, error="composer_not_found")
    sent = await CamofoxInteractions(page).press(MESSAGE_COMPOSER, "Enter")
    return SendMessageOutput(
        sent=sent,
        thread_id=data.thread_id,
        error=None if sent else "send_failed",
    )
