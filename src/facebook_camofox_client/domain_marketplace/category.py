"""Marketplace category selection primitive."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import CATEGORY


async def set_category(page: Any, category: str) -> bool:
    interactions = CamofoxInteractions(page)
    if not await interactions.click(CATEGORY):
        return False
    option = page.locator("[role='option']", has_text=category).first()
    if await option.count() == 0:
        option = page.get_by_text(category, exact=True).first()
    if await option.count() == 0:
        return False
    await option.click()
    return True
