"""RFC 6238 TOTP generation for account authentication challenges."""
from __future__ import annotations

import base64
import hashlib
import hmac
import struct
import time


def generate_totp(secret: str, timestamp: int | None = None, period: int = 30) -> str:
    """Return the six-digit TOTP for an account-owned secret."""
    normalized = "".join(secret.split()).upper()
    padding = "=" * (-len(normalized) % 8)
    key = base64.b32decode(normalized + padding, casefold=True)
    counter = int((time.time() if timestamp is None else timestamp) // period)
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    return f"{code % 1_000_000:06d}"
