"""Marketplace condition selection primitive."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import CONDITION


async def set_condition(page: Any, condition: str) -> bool:
    interactions = CamofoxInteractions(page)
    if not await interactions.click(CONDITION):
        return False
    for candidate in (condition, "Used – good", "Used - Good", "Used – like new", "New"):
        try:
            option = page.locator("[role='option']", has_text=candidate).first()
            if await option.count() == 0:
                option = page.get_by_text(candidate, exact=True).first()
            if await option.count() > 0:
                await option.click()
                return True
        except Exception:
            continue
    return False
