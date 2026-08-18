from facebook_camofox_client.domain_accounts.totp import generate_totp


def test_generate_totp_rfc6238_sha1_vector() -> None:
    # RFC 6238 SHA-1 test secret, represented as Base32 for the client API.
    secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
    assert generate_totp(secret, timestamp=59) == "287082"
