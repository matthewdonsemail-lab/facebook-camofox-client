"""Adapter to wire Facebook domain actions into OpenMagpie."""
from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from typing import ClassVar

from facebook_camofox_client.domain_actions.envelope import ActionEnvelope
from facebook_camofox_client.domain_actions.runner import ActionRunner
from facebook_camofox_client.domain_accounts.login import FacebookLogin
from facebook_camofox_client.domain_camofox.session_manager import CamofoxSessionManager
from facebook_camofox_client.domain_cursors.repository import InMemoryCursorRepository
from facebook_camofox_client.domain_events.emitter import InMemoryEventEmitter
from facebook_camofox_client.domain_groups.search import GroupsSearchAction
from facebook_camofox_client.domain_marketplace.create import create_listing
from facebook_camofox_client.domain_marketplace.schemas import MarketplaceListingInput
from facebook_camofox_client.domain_messenger.send import send_message
from facebook_camofox_client.domain_messenger.schemas import SendMessageInput
from facebook_camofox_client.domain_records.normalization import PostNormalizer


class FacebookCamofoxConnector:
    kind: ClassVar[str] = "facebook_search"

    def __init__(self) -> None:
        self.runner = ActionRunner()
        self.session_manager = CamofoxSessionManager()
        self.cursor_repo = InMemoryCursorRepository()
        self.emitter = InMemoryEventEmitter()
        self.normalizer = PostNormalizer()

        search = GroupsSearchAction(
            self.session_manager,
            self.cursor_repo,
            self.normalizer,
            self.emitter,
        )
        self.runner.register("groups.search", search.execute)
        self.runner.register("account.login", self._login)
        self.runner.register("messenger.send", self._send_message)
        self.runner.register("marketplace.create", self._create_listing)

    async def _login(self, envelope: ActionEnvelope) -> dict:
        session = await self.session_manager.acquire(
            envelope.account_id,
            proxy_config=envelope.input.get("proxy_config"),
            storage_state_path=envelope.input.get("storage_state_path"),
        )
        try:
            page = await session.open_surface("facebook_messages")
            return await FacebookLogin().execute(
                page,
                email=envelope.input["email"],
                password=envelope.input["password"],
                totp_secret=envelope.input.get("totp_secret"),
            )
        finally:
            await self.session_manager.release(session)

    async def _send_message(self, envelope: ActionEnvelope) -> dict:
        session = await self.session_manager.acquire(
            envelope.account_id,
            proxy_config=envelope.input.get("proxy_config"),
            storage_state_path=envelope.input.get("storage_state_path"),
        )
        try:
            page = await session.open_surface("facebook_messages")
            return (await send_message(page, SendMessageInput(**envelope.input))).model_dump()
        finally:
            await self.session_manager.release(session)

    async def _create_listing(self, envelope: ActionEnvelope) -> dict:
        session = await self.session_manager.acquire(
            envelope.account_id,
            proxy_config=envelope.input.get("proxy_config"),
            storage_state_path=envelope.input.get("storage_state_path"),
        )
        try:
            result = await create_listing(session, MarketplaceListingInput(**envelope.input))
            return result.model_dump()
        finally:
            await self.session_manager.release(session)

    async def poll(self, spec: dict, since: datetime | None = None) -> Iterator[dict]:
        envelope = ActionEnvelope(
            action_id=f"poll-{datetime.now().timestamp()}",
            action_type="groups.search",
            account_id=spec.get("account_id", "default"),
            input=spec,
            idempotency_key=f"poll-{spec.get('page_url', '')}-{since}",
        )
        result = await self.runner.run(envelope)
        for record in result.get("results", []):
            yield record
