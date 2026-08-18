# Facebook action parity

This client ports the proven Facebook behaviors - Camofox-native domain architecture.

## Architecture

```text
ActionEnvelope
  -> ActionRunner / ActionRegistry
  -> domain action
  -> CamofoxSessionManager
  -> CamofoxSession
  -> CamofoxInteractions
  -> Facebook surface
  -> normalized result / event / cursor
```

The Facebook client does not import the `playwright` package. Browser interaction is isolated behind `domain_camofox` and the Camoufox runtime.

## Domain layout

```text
src/facebook_camofox_client/
├── domain_accounts/
│   ├── auth_guard.py
│   ├── challenges.py
│   ├── login.py
│   ├── models.py
│   └── totp.py
├── domain_actions/
│   ├── envelope.py
│   ├── registry.py
│   └── runner.py
├── domain_camofox/
│   ├── constants.py
│   ├── interactions.py
│   ├── navigation.py
│   ├── selectors.py
│   ├── session.py
│   └── session_manager.py
├── domain_connectors/
├── domain_cursors/
├── domain_events/
├── domain_groups/
├── domain_marketplace/
│   ├── category.py
│   ├── condition.py
│   ├── create.py
│   ├── fields.py
│   ├── images.py
│   ├── publish.py
│   ├── schemas.py
│   └── validation.py
├── domain_messenger/
│   ├── compose.py
│   ├── messages.py
│   ├── open.py
│   ├── schemas.py
│   ├── send.py
│   └── threads.py
├── domain_records/
└── domain_runtime/
```

## Source parity

- `agent/src/adspower.ts` — account/browser profile lifecycle.
- `agent/src/login-accounts.ts` — Facebook login, OTP challenge detection and submission.
- `agent/src/fix-logins.ts` — remembered-profile and login recovery paths.
- `agent/src/inbox-monitor.ts` — Messenger thread discovery, message extraction and sending.
- `agent/src/poster.ts` — Marketplace form, image upload, Next/Publish and confirmation workflow.

The new client intentionally ports the *domain behavior* and keeps browser-driver mechanics behind Camofox. Selectors are semantic candidates in `domain_camofox/selectors.py`; domain actions do not import or instantiate a Playwright client.

## Action names

- `account.login`
- `groups.search`
- `messenger.send`
- `marketplace.create`

The existing group-search action remains registered and now shares the same session/runtime boundary as the new actions.

## Camofox runtime

The session manager keeps the existing account-scoped runtime behavior: `humanize=True`, `geoip=True`, optional proxy configuration, and optional persisted `storage_state`. Those values live in `domain_camofox/constants.py` and are consumed only by `domain_camofox/session_manager.py`.
