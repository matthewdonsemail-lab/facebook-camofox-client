"""Marketplace listing creation action."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.constants import SURFACE_MARKETPLACE
from .category import set_category
from .condition import set_condition
from .fields import set_description, set_price, set_title
from .images import upload_images
from .publish import publish
from .schemas import MarketplaceListingInput, MarketplaceListingOutput
from .validation import validate_available


async def create_listing(session: Any, data: MarketplaceListingInput) -> MarketplaceListingOutput:
    page = await session.open_surface(SURFACE_MARKETPLACE)
    available, error = await validate_available(page)
    if not available:
        return MarketplaceListingOutput(published=False, error=error)

    if not await upload_images(page, data.image_paths):
        return MarketplaceListingOutput(published=False, error="image_upload_failed")
    if not await set_title(page, data.title):
        return MarketplaceListingOutput(published=False, error="title_not_filled")
    if not await set_price(page, data.price):
        return MarketplaceListingOutput(published=False, error="price_not_filled")
    if not await set_category(page, data.category):
        return MarketplaceListingOutput(published=False, error="category_not_selected")
    if not await set_condition(page, data.condition):
        return MarketplaceListingOutput(published=False, error="condition_not_selected")
    if data.description and not await set_description(page, data.description):
        return MarketplaceListingOutput(published=False, error="description_not_filled")

    result = await publish(page)
    return MarketplaceListingOutput(**result)
