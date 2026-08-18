"""Marketplace image upload primitive."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import MARKETPLACE_IMAGE_INPUT


async def upload_images(page: Any, image_paths: list[str]) -> bool:
    if not image_paths:
        return True
    return await CamofoxInteractions(page).upload(MARKETPLACE_IMAGE_INPUT, image_paths)
