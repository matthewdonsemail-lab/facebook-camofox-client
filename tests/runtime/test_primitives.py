from __future__ import annotations

import logging
import os

import pytest

from facebook_camofox_client.domain_actions.envelope import ActionEnvelope
from facebook_camofox_client.domain_connectors.openmagpie import FacebookCamofoxConnector

LOGGER = logging.getLogger("facebook-camofox.runtime")


def _proxy(config: dict[str, str | None]) -> dict[str, str] | None:
    if not config.get("proxy_server"):
        return None
    result = {"server": config["proxy_server"]}
    if config.get("proxy_username"):
        result["username"] = config["proxy_username"]
    if config.get("proxy_password"):
        result["password"] = config["proxy_password"]
    return result


def _common_input(runtime_config: dict[str, str | None]) -> dict[str, object]:
    return {
        "proxy_config": _proxy(runtime_config),
        "storage_state_path": runtime_config["storage_state_path"],
    }


@pytest.mark.asyncio
async def test_account_login_is_real_runtime_action(runtime_config):
    connector = FacebookCamofoxConnector()
    LOGGER.info("[account.login] acquiring account-scoped Camofox runtime")
    input_data = _common_input(runtime_config)
    input_data.update(
        {
            "email": runtime_config["email"],
            "password": runtime_config["password"],
            "totp_secret": runtime_config["totp_secret"],
        }
    )
    envelope = ActionEnvelope(
        action_id="runtime-account-login",
        action_type="account.login",
        account_id=runtime_config["account_id"],
        input=input_data,
        idempotency_key="runtime-account-login",
    )
    LOGGER.info("[account.login] executing Facebook authentication primitive")
    result = await connector.runner.run(envelope)
    LOGGER.info("[account.login] completed status=%s result=%s", envelope.status, result)
    assert result.get("authenticated") is True


@pytest.mark.asyncio
async def test_messenger_send_is_real_runtime_action(runtime_config):
    thread_id = os.getenv("FACEBOOK_RUNTIME_THREAD_ID")
    thread_name = os.getenv("FACEBOOK_RUNTIME_THREAD_NAME")
    text = os.getenv("FACEBOOK_RUNTIME_MESSAGE")
    if not text or not (thread_id or thread_name):
        pytest.fail(
            "FACEBOOK_RUNTIME_THREAD_ID or FACEBOOK_RUNTIME_THREAD_NAME and "
            "FACEBOOK_RUNTIME_MESSAGE are required for the real Messenger action"
        )

    connector = FacebookCamofoxConnector()
    input_data = _common_input(runtime_config)
    input_data.update({"thread_id": thread_id, "thread_name": thread_name, "text": text})
    envelope = ActionEnvelope(
        action_id="runtime-messenger-send",
        action_type="messenger.send",
        account_id=runtime_config["account_id"],
        input=input_data,
        idempotency_key="runtime-messenger-send",
    )
    LOGGER.info("[messenger.send] opening target conversation and sending configured runtime message")
    result = await connector.runner.run(envelope)
    LOGGER.info("[messenger.send] completed status=%s result=%s", envelope.status, result)
    assert result.get("sent") is True


@pytest.mark.asyncio
async def test_marketplace_create_is_real_runtime_action(runtime_config):
    title = os.getenv("FACEBOOK_RUNTIME_MARKETPLACE_TITLE")
    price = os.getenv("FACEBOOK_RUNTIME_MARKETPLACE_PRICE")
    images = os.getenv("FACEBOOK_RUNTIME_MARKETPLACE_IMAGES")
    if not title or not price or not images:
        pytest.fail(
            "FACEBOOK_RUNTIME_MARKETPLACE_TITLE, FACEBOOK_RUNTIME_MARKETPLACE_PRICE and "
            "FACEBOOK_RUNTIME_MARKETPLACE_IMAGES are required for the real Marketplace action"
        )

    connector = FacebookCamofoxConnector()
    input_data = _common_input(runtime_config)
    input_data.update(
        {
            "title": title,
            "price": price,
            "category": os.getenv("FACEBOOK_RUNTIME_MARKETPLACE_CATEGORY", "Miscellaneous"),
            "condition": os.getenv("FACEBOOK_RUNTIME_MARKETPLACE_CONDITION", "Used - Good"),
            "description": os.getenv("FACEBOOK_RUNTIME_MARKETPLACE_DESCRIPTION", ""),
            "image_paths": [item for item in images.split(os.pathsep) if item],
        }
    )
    envelope = ActionEnvelope(
        action_id="runtime-marketplace-create",
        action_type="marketplace.create",
        account_id=runtime_config["account_id"],
        input=input_data,
        idempotency_key="runtime-marketplace-create",
    )
    LOGGER.info("[marketplace.create] executing real listing creation primitive")
    result = await connector.runner.run(envelope)
    LOGGER.info("[marketplace.create] completed status=%s result=%s", envelope.status, result)
    assert result.get("published") is True
