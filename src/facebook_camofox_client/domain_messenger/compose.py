"""Messenger composer primitives."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import MESSAGE_COMPOSER


async def compose_message(page: Any, text: str) -> bool:
    interactions = CamofoxInteractions(page)
    if await interactions.fill(MESSAGE_COMPOSER, text):
        return True
    return await interactions.type_text(MESSAGE_COMPOSER, text)
