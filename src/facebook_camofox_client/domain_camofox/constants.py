"""Camofox runtime constants and supported Facebook surfaces."""

CAMOFOX_HUMANIZE = True
CAMOFOX_GEOIP = True

FACEBOOK_BASE_URL = "https://www.facebook.com"
FACEBOOK_LOGIN_URL = f"{FACEBOOK_BASE_URL}/login"
FACEBOOK_MARKETPLACE_CREATE_URL = f"{FACEBOOK_BASE_URL}/marketplace/create/item"
FACEBOOK_MESSAGES_URL = f"{FACEBOOK_BASE_URL}/messages/t/"

SURFACE_GROUP = "facebook_group"
SURFACE_MESSAGES = "facebook_messages"
SURFACE_MARKETPLACE = "facebook_marketplace"

SUPPORTED_SURFACES = {
    SURFACE_GROUP,
    SURFACE_MESSAGES,
    SURFACE_MARKETPLACE,
}
