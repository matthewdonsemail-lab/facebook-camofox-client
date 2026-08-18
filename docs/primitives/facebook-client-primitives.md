---
title: Facebook Client Primitive Execution Map
description: Production runtime contract and evidence map for every Facebook Camofox primitive.
---

# Facebook client primitive execution map

This document is the executable contract for the Facebook Camofox client. Every primitive must have a documented execution sequence and a runtime test. When a primitive changes, this document must be updated in the same change.

## Account

### account.login

Execution sequence:

1. Acquire the account-scoped Camofox session.
2. Open the Facebook authentication surface.
3. Inspect the page for an existing authenticated state.
4. Locate the email input using the semantic account selector.
5. Enter the configured email.
6. Locate the password input.
7. Enter the configured password.
8. Submit login.
9. Wait for the resulting Facebook state.
10. Detect whether Facebook presents a challenge.
11. If an OTP challenge is present, generate the RFC 6238 TOTP from the configured secret.
12. Enter the six-digit OTP into the challenge field.
13. Submit the challenge.
14. Dismiss the save-login/remember-device surface when present.
15. Assert that the account is authenticated.

Evidence: `Listaro_backup/agent/src/login-accounts.ts`, `Listaro_backup/agent/src/fix-logins.ts`.

## Messenger

### messenger.capture_threads

1. Acquire an authenticated account-scoped session.
2. Open Facebook Messages.
3. Confirm the account is authenticated.
4. Locate the conversation sidebar.
5. Enumerate thread links.
6. Extract stable thread identity and preview metadata.
7. Return normalized thread records.

Evidence: `Listaro_backup/agent/src/inbox-monitor.ts`.

### messenger.capture_thread

1. Open the target thread from the conversation surface.
2. Wait for the message panel.
3. Locate the message collection.
4. Extract message text and direction.
5. Remove timestamps/system labels from normalized message content.
6. Return ordered message records.

Evidence: `Listaro_backup/agent/src/inbox-monitor.ts`.

### messenger.send

1. Open the target conversation.
2. Locate the visible contenteditable composer.
3. Focus the composer.
4. Insert the message using the Camofox-native text primitive.
5. Verify the composer contains the intended text.
6. Submit the message.
7. Verify the message appears as sent.

Evidence: `Listaro_backup/agent/src/inbox-monitor.ts`.

## Marketplace

### marketplace.create

1. Acquire the account-scoped Camofox session.
2. Open Marketplace create.
3. Dismiss known blocking surfaces.
4. Assert Marketplace is available and the account is authenticated.
5. Check ban/rate-limit/identity-verification states.
6. Select Item for Sale.
7. Upload configured images.
8. Set title.
9. Set price.
10. Select category.
11. Select condition.
12. Set description.
13. Advance through Next surfaces until publish is available.
14. Publish the listing.
15. Wait for the confirmation surface.
16. Extract and return the listing URL/identifier.

Evidence: `Listaro_backup/agent/src/poster.ts`.

## Camofox boundary

No domain primitive may import Playwright. Domain actions use semantic targets and the Camofox interaction layer. Camofox is responsible for browser lifecycle, humanization, geo-IP configuration, proxy configuration and persisted browser state.

## Runtime evidence requirements

Runtime tests are real execution tests. They must not be named or implemented as `smoke_tests`, must not mock the browser, and must emit actionable logs for each execution step. Secrets, cookies, storage state and TOTP values must never be logged.
