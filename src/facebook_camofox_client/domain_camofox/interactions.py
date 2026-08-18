"""Camofox-native browser interaction primitives.

Domain modules depend on these semantic operations rather than a browser-driver
implementation. No Playwright package is imported by the Facebook client.
"""
from __future__ import annotations

from typing import Any, Iterable


class CamofoxInteractionError(RuntimeError):
    """Raised when a Camofox interaction cannot be completed."""


class CamofoxInteractions:
    def __init__(self, page: Any) -> None:
        self.page = page

    async def goto(self, url: str, wait_until: str = "domcontentloaded") -> Any:
        return await self.page.goto(url, wait_until=wait_until)

    async def click(self, selectors: Iterable[str], *, timeout: int = 5000) -> bool:
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first()
                if await locator.count() > 0:
                    await locator.click(timeout=timeout)
                    return True
            except Exception:
                continue
        return False

    async def fill(self, selectors: Iterable[str], value: str, *, timeout: int = 5000) -> bool:
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first()
                if await locator.count() > 0:
                    await locator.fill(value, timeout=timeout)
                    return True
            except Exception:
                continue
        return False

    async def press(self, selectors: Iterable[str], key: str, *, timeout: int = 5000) -> bool:
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first()
                if await locator.count() > 0:
                    await locator.press(key, timeout=timeout)
                    return True
            except Exception:
                continue
        return False

    async def type_text(self, selectors: Iterable[str], value: str, *, timeout: int = 5000) -> bool:
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first()
                if await locator.count() > 0:
                    await locator.click(timeout=timeout)
                    await self.page.keyboard.type(value)
                    return True
            except Exception:
                continue
        return False

    async def text(self, selectors: Iterable[str]) -> str:
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first()
                if await locator.count() > 0:
                    return await locator.inner_text()
            except Exception:
                continue
        return ""

    async def value(self, selectors: Iterable[str]) -> str:
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first()
                if await locator.count() > 0:
                    return await locator.input_value()
            except Exception:
                continue
        return ""

    async def exists(self, selectors: Iterable[str]) -> bool:
        for selector in selectors:
            try:
                if await self.page.locator(selector).first().count() > 0:
                    return True
            except Exception:
                continue
        return False

    async def upload(self, selectors: Iterable[str], files: list[str], *, timeout: int = 5000) -> bool:
        for selector in selectors:
            try:
                locator = self.page.locator(selector).first()
                if await locator.count() > 0:
                    await locator.set_input_files(files, timeout=timeout)
                    return True
            except Exception:
                continue
        return False

    async def body_text(self) -> str:
        return await self.page.locator("body").inner_text()

    async def url(self) -> str:
        return self.page.url
