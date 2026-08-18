from __future__ import annotations

import logging

import pytest

from facebook_camofox_client.domain_actions.envelope import ActionEnvelope
from facebook_camofox_client.domain_connectors.openmagpie import FacebookCamofoxConnector

LOGGER = logging.getLogger("facebook_camofox.runtime")


def _proxy(config: dict[str, str | None]) -> dict[str, str] | None:
    if not config.get("proxy_server"):
        return None
    result = {"server": config["proxy_server"]}
    if config.get("proxy_username"):
        result["username"] = config["proxy_username"]
    if config.get("proxy_password"):
        result["password"] = config["proxy_password"]
    return result


@pytest.mark.asyncio
async def test_account_login_is_real_runtime_action(runtime_config):
    connector = FacebookCamofoxConnector()
    LOGGER.info("[account.login] acquiring account-scoped Camofox runtime")
    envelope = ActionEnvelope(
        action_id="runtime-account-login",
        action_type="account.login",
        account_id=runtime_config["account_id"],
        input={
            "email": runtime_config["email"],
            "password": runtime_config["password"],
            "totp_secret": runtime_config["totp_secret"],
            "proxy_config": _proxy(runtime_config),
            "storage_state_path": runtime_config["storage_state_path"],
        },
        idempotency_key="runtime-account-login",
    )
    LOGGER.info("[account.login] executing Facebook authentication primitive")
    result = await connector.runner.run(envelope)
    LOGGER.info("[account.login] result status=%s", envelope.status)
    assert result.get("authenticated") is True


@pytest.mark.asyncio
async def test_messenger_send_is_real_runtime_action(runtime_config):
    connector = FacebookCamofoxConnector()
    LOGGER.info("[messenger.send] executing real message primitive")
    pytest.fail("Runtime fixture requires a configured target thread/message input before execution")


@pytest.mark.asyncio
async def test_marketplace_create_is_real_runtime_action(runtime_config):
    connector = FacebookCamofoxConnector()
    LOGGER.info("[marketplace.create] executing real Marketplace primitive")
    pytest.fail("Runtime fixture requires configured listing/image input before execution")
