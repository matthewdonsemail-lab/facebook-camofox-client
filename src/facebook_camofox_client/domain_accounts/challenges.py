"""Authentication challenge detection and resolution primitives."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from facebook_camofox_client.domain_camofox.interactions import CamofoxInteractions
from facebook_camofox_client.domain_camofox.selectors import OTP
from .totp import generate_totp


@dataclass(frozen=True)
class ChallengeResult:
    required: bool
    resolved: bool = False
    reason: str | None = None


class AuthenticationChallenges:
    async def detect(self, page: Any) -> ChallengeResult:
        interactions = CamofoxInteractions(page)
        body = (await interactions.body_text()).lower()
        required = (
            "two-factor" in body
            or "two factor" in body
            or "authentication code" in body
            or await interactions.exists(OTP)
        )
        return ChallengeResult(required=required)

    async def resolve_totp(self, page: Any, secret: str) -> ChallengeResult:
        interactions = CamofoxInteractions(page)
        code = generate_totp(secret)
        filled = await interactions.fill(OTP, code)
        if not filled:
            filled = await interactions.type_text(OTP, code)
        if not filled:
            return ChallengeResult(required=True, reason="otp_field_not_found")
        submitted = await interactions.press(OTP, "Enter")
        return ChallengeResult(required=True, resolved=submitted, reason=None if submitted else "otp_submit_failed")
