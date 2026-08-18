"""Marketplace form-field primitives."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import DESCRIPTION, PRICE, TITLE


async def set_title(page: Any, value: str) -> bool:
    return await CamofoxInteractions(page).fill(TITLE, value)


async def set_price(page: Any, value: str) -> bool:
    return await CamofoxInteractions(page).fill(PRICE, value)


async def set_description(page: Any, value: str) -> bool:
    return await CamofoxInteractions(page).fill(DESCRIPTION, value)
