"""Facebook login action primitives for account-owned sessions."""
from __future__ import annotations

from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import LOGIN_EMAIL, LOGIN_PASSWORD, LOGIN_SUBMIT
from facebook_camofox_client.domain_camofox.constants import FACEBOOK_LOGIN_URL
from .auth_guard import AuthGuard, AuthState
from .challenges import AuthenticationChallenges


class FacebookLogin:
    def __init__(self) -> None:
        self.auth_guard = AuthGuard()
        self.challenges = AuthenticationChallenges()

    async def execute(
        self,
        page: Any,
        email: str,
        password: str,
        totp_secret: str | None = None,
    ) -> dict[str, Any]:
        interactions = CamofoxInteractions(page)
        await interactions.goto(FACEBOOK_LOGIN_URL)
        if not await interactions.fill(LOGIN_EMAIL, email):
            return {"authenticated": False, "error": "email_field_not_found"}
        if not await interactions.fill(LOGIN_PASSWORD, password):
            return {"authenticated": False, "error": "password_field_not_found"}
        if not await interactions.click(LOGIN_SUBMIT):
            if not await interactions.press(LOGIN_PASSWORD, "Enter"):
                return {"authenticated": False, "error": "login_submit_failed"}

        challenge = await self.challenges.detect(page)
        if challenge.required:
            if not totp_secret:
                return {"authenticated": False, "error": "two_factor_required"}
            resolved = await self.challenges.resolve_totp(page, totp_secret)
            if not resolved.resolved:
                return {"authenticated": False, "error": resolved.reason or "two_factor_failed"}

        result = await self.auth_guard.validate(await page.title(), page.url)
        return {"authenticated": result.state == AuthState.authenticated, "state": result.state.value}
