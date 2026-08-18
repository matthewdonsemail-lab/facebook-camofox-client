"""Marketplace state validation primitives."""
from __future__ import annotations

from typing import Any


RATE_LIMIT_PHRASES = ("rate limit", "too many", "try again later")
VERIFY_IDENTITY_PHRASES = ("verify your identity", "identity verification")
BAN_PHRASES = ("marketplace access is restricted", "marketplace isn't available")
SUCCESS_PHRASES = ("your listing is published", "listed on marketplace", "your item is now listed")


async def page_text(page: Any) -> str:
    return (await page.locator("body").inner_text()).lower()


async def validate_available(page: Any) -> tuple[bool, str | None]:
    text = await page_text(page)
    for phrase in BAN_PHRASES:
        if phrase in text:
            return False, "marketplace_unavailable"
    return True, None


async def validate_publish_state(page: Any) -> tuple[bool, str | None]:
    text = await page_text(page)
    for phrase in RATE_LIMIT_PHRASES:
        if phrase in text:
            return False, "rate_limit"
    for phrase in VERIFY_IDENTITY_PHRASES:
        if phrase in text:
            return False, "verify_identity"
    return True, None
