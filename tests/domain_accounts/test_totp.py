from facebook_camofox_client.domain_accounts.totp import generate_totp


def test_generate_totp_rfc6238_sha1_vector() -> None:
    # RFC 6238 test secret for SHA-1.
    secret = "12345678901234567890"
    assert generate_totp(secret, timestamp=59) == "94287082"
