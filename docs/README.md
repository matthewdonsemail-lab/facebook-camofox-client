---
title: Facebook Camofox Client Documentation
description: Production documentation and executable primitive contracts.
---

# Facebook Camofox Client Documentation

Documentation uses YAML frontmatter so every document has machine-readable ownership and purpose.

## Primitive contract

The canonical primitive map is [`primitives/facebook-client-primitives.md`](./primitives/facebook-client-primitives.md).

A primitive change is incomplete unless its documented execution sequence and runtime evidence are updated in the same change.

## Source parity

The behavioral reference is `Listaro_backup`. The implementation target is the Camofox-native client. Playwright is source evidence only; it is not a runtime dependency or domain abstraction in this project.
