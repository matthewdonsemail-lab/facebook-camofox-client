"""Marketplace Next/Publish primitives."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import NEXT, PUBLISH
from .validation import SUCCESS_PHRASES, validate_publish_state


async def next_step(page: Any) -> bool:
    return await CamofoxInteractions(page).click(NEXT)


async def publish(page: Any, max_intermediate_pages: int = 4) -> dict[str, Any]:
    interactions = CamofoxInteractions(page)
    for _ in range(max_intermediate_pages + 1):
        ok, error = await validate_publish_state(page)
        if not ok:
            return {"published": False, "error": error}
        if await interactions.click(PUBLISH):
            for _ in range(30):
                text = await interactions.body_text()
                lowered = text.lower()
                if any(phrase in lowered for phrase in SUCCESS_PHRASES) or "/marketplace/item/" in page.url:
                    link = page.locator("a[href*='/marketplace/item/']").first()
                    listing_url = await link.get_attribute("href") if await link.count() > 0 else page.url
                    if listing_url and listing_url.startswith("/"):
                        listing_url = f"https://www.facebook.com{listing_url}"
                    return {"published": True, "listing_url": listing_url}
                await page.wait_for_timeout(1000)
            return {"published": False, "error": "no_confirmation"}
        if not await next_step(page):
            break
        await page.wait_for_timeout(1000)
    return {"published": False, "error": "publish_button_not_found"}
