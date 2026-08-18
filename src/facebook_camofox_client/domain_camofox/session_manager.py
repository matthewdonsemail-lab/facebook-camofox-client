"""Account-scoped Camofox runtime lifecycle."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .constants import CAMOFOX_GEOIP, CAMOFOX_HUMANIZE
from .session import CamofoxSession


class CamofoxSessionManager:
    async def acquire(
        self,
        account_id: str,
        proxy_config: dict[str, Any] | None = None,
        storage_state_path: str | None = None,
    ) -> CamofoxSession:
        from camoufox.async_api import AsyncCamoufox

        runtime = AsyncCamoufox(
            humanize=CAMOFOX_HUMANIZE,
            geoip=CAMOFOX_GEOIP,
            proxy=proxy_config,
        )
        browser = await runtime.__aenter__()
        context_kwargs: dict[str, Any] = {}
        if storage_state_path:
            context_kwargs["storage_state"] = str(Path(storage_state_path))
        context = await browser.new_context(**context_kwargs)
        return CamofoxSession(account_id, runtime, browser, context)

    async def release(self, session: CamofoxSession) -> None:
        if session._closed:
            return
        session._closed = True
        try:
            await session.context.close()
        finally:
            await session.runtime.__aexit__(None, None, None)
